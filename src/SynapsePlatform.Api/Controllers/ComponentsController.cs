using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using SynapsePlatform.Api.DTOs;
using SynapsePlatform.Core.Entities;
using SynapsePlatform.Core.Enums;
using SynapsePlatform.Core.Interfaces;
using SynapsePlatform.Infrastructure.Data;

namespace SynapsePlatform.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class ComponentsController : ControllerBase
{
    private readonly SynapseDbContext _context;
    private readonly IIDIService _idiService;

    public ComponentsController(SynapseDbContext context, IIDIService idiService)
    {
        _context = context;
        _idiService = idiService;
    }

    [HttpGet]
    public async Task<ActionResult<IEnumerable<ComponentDto>>> GetComponents([FromQuery] Guid projectId)
    {
        var components = await _context.Components
            .Where(c => c.ProjectId == projectId)
            .ToListAsync();

        return Ok(components.Select(c => new ComponentDto(
            c.Id, c.Name, c.Description, c.Type, c.ComponentIDI,
            GetIDIStatus(c.ComponentIDI), c.DaysSinceLastIntegration,
            c.LastIntegrationDate, c.LinesOfCodeChanged, c.DependencyCount,
            c.PowerBudgetWatts, c.ActualPowerWatts
        )));
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<ComponentDto>> GetComponent(Guid id)
    {
        var c = await _context.Components.FindAsync(id);
        if (c == null) return NotFound();

        return Ok(new ComponentDto(
            c.Id, c.Name, c.Description, c.Type, c.ComponentIDI,
            GetIDIStatus(c.ComponentIDI), c.DaysSinceLastIntegration,
            c.LastIntegrationDate, c.LinesOfCodeChanged, c.DependencyCount,
            c.PowerBudgetWatts, c.ActualPowerWatts
        ));
    }

    [HttpPost]
    public async Task<ActionResult<ComponentDto>> CreateComponent(CreateComponentDto dto)
    {
        var component = new Component
        {
            Name = dto.Name,
            Description = dto.Description,
            Type = dto.Type,
            ProjectId = dto.ProjectId,
            PowerBudgetWatts = dto.PowerBudgetWatts,
            LatencyThresholdMs = dto.LatencyThresholdMs,
            MemoryLimitMB = dto.MemoryLimitMB
        };

        _context.Components.Add(component);
        await _context.SaveChangesAsync();

        return CreatedAtAction(nameof(GetComponent), new { id = component.Id }, new ComponentDto(
            component.Id, component.Name, component.Description, component.Type,
            0, IDIStatus.Healthy, 0, null, 0, 0, component.PowerBudgetWatts, null
        ));
    }

    [HttpPost("{id}/integrate")]
    public async Task<IActionResult> RecordIntegration(Guid id, [FromBody] RecordIntegrationRequest request)
    {
        var component = await _context.Components.FindAsync(id);
        if (component == null) return NotFound();

        var idiBeforeIntegration = _idiService.CalculateComponentIDI(component);

        component.LastIntegrationDate = DateTime.UtcNow;
        component.LinesOfCodeChanged = 0;
        component.DaysSinceLastIntegration = 0;
        component.IsIntegrated = true;
        component.UpdatedAt = DateTime.UtcNow;

        var record = new IntegrationRecord
        {
            ProjectId = component.ProjectId,
            ComponentId = id,
            IntegrationDate = DateTime.UtcNow,
            WasSuccessful = request.WasSuccessful,
            IDIBeforeIntegration = idiBeforeIntegration,
            IDIAfterIntegration = 0,
            LinesOfCodeIntegrated = request.LinesOfCodeIntegrated,
            IssuesFound = request.IssuesFound,
            IssuesResolved = request.IssuesResolved,
            Notes = request.Notes,
            Duration = TimeSpan.FromMinutes(request.DurationMinutes)
        };

        _context.IntegrationRecords.Add(record);
        await _context.SaveChangesAsync();

        return Ok(new { Message = "Integration recorded successfully", NewIDI = 0.0 });
    }

    [HttpGet("needs-integration")]
    public async Task<ActionResult<IEnumerable<ComponentDto>>> GetComponentsNeedingIntegration([FromQuery] Guid projectId)
    {
        var components = await _idiService.GetComponentsNeedingIntegrationAsync(projectId);

        return Ok(components.Select(c => new ComponentDto(
            c.Id, c.Name, c.Description, c.Type, c.ComponentIDI,
            GetIDIStatus(c.ComponentIDI), c.DaysSinceLastIntegration,
            c.LastIntegrationDate, c.LinesOfCodeChanged, c.DependencyCount,
            c.PowerBudgetWatts, c.ActualPowerWatts
        )));
    }

    private static IDIStatus GetIDIStatus(double idi)
    {
        if (idi < 3.0) return IDIStatus.Healthy;
        if (idi <= 5.0) return IDIStatus.Warning;
        return IDIStatus.Critical;
    }
}

public record RecordIntegrationRequest(
    bool WasSuccessful,
    int LinesOfCodeIntegrated,
    int IssuesFound,
    int IssuesResolved,
    string? Notes,
    int DurationMinutes
);
