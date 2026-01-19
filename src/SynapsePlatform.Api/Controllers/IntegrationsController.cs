using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using SynapsePlatform.Api.DTOs;
using SynapsePlatform.Core.Interfaces;
using SynapsePlatform.Infrastructure.Data;

namespace SynapsePlatform.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class IntegrationsController : ControllerBase
{
    private readonly IIDIService _idiService;
    private readonly SynapseDbContext _context;

    public IntegrationsController(IIDIService idiService, SynapseDbContext context)
    {
        _idiService = idiService;
        _context = context;
    }

    [HttpGet]
    public async Task<ActionResult<IEnumerable<IntegrationRecordDto>>> GetIntegrations([FromQuery] Guid projectId)
    {
        var records = await _context.IntegrationRecords
            .Where(r => r.ProjectId == projectId)
            .Include(r => r.PerformedBy)
            .OrderByDescending(r => r.IntegrationDate)
            .ToListAsync();

        return Ok(records.Select(r => new IntegrationRecordDto(
            r.Id,
            r.IntegrationDate,
            r.IDIBeforeIntegration,
            r.IDIAfterIntegration,
            r.ComponentsIntegrated,
            r.LinesOfCodeIntegrated,
            r.WasSuccessful,
            r.PerformedBy?.FullName
        )));
    }

    [HttpPost]
    public async Task<ActionResult<IntegrationRecordDto>> RecordIntegration(RecordIntegrationDto dto)
    {
        var record = await _idiService.RecordIntegrationAsync(
            dto.ProjectId,
            dto.ComponentIds,
            dto.Description
        );

        return CreatedAtAction(
            nameof(GetIntegrations),
            new { projectId = dto.ProjectId },
            new IntegrationRecordDto(
                record.Id,
                record.IntegrationDate,
                record.IDIBeforeIntegration,
                record.IDIAfterIntegration,
                record.ComponentsIntegrated,
                record.LinesOfCodeIntegrated,
                record.WasSuccessful,
                null
            )
        );
    }

    [HttpGet("project/{projectId}/idi")]
    public async Task<ActionResult<object>> GetProjectIDI(Guid projectId)
    {
        var project = await _context.Projects
            .Include(p => p.Components)
            .FirstOrDefaultAsync(p => p.Id == projectId);

        if (project == null)
            return NotFound();

        var idi = _idiService.CalculateProjectIDI(project);
        var status = _idiService.GetHealthStatus(idi);
        var mandatory = _idiService.IsIntegrationMandatory(idi);

        return Ok(new
        {
            ProjectId = projectId,
            CurrentIDI = Math.Round(idi, 2),
            Status = status.ToString(),
            IsIntegrationMandatory = mandatory,
            MaxAllowedIDI = project.MaxAllowedIDI,
            ComponentCount = project.Components.Count,
            IntegratedCount = project.Components.Count(c => c.IsIntegrated)
        });
    }

    [HttpGet("project/{projectId}/component-idi")]
    public async Task<ActionResult<IEnumerable<object>>> GetComponentIDIs(Guid projectId)
    {
        var components = await _context.Components
            .Where(c => c.ProjectId == projectId)
            .ToListAsync();

        return Ok(components.Select(c =>
        {
            var idi = _idiService.CalculateComponentIDI(c);
            return new
            {
                ComponentId = c.Id,
                ComponentName = c.Name,
                ComponentType = c.Type.ToString(),
                IDI = Math.Round(idi, 2),
                Status = _idiService.GetHealthStatus(idi).ToString(),
                DaysSinceIntegration = c.DaysSinceLastIntegration,
                LinesChanged = c.LinesOfCodeChanged,
                Dependencies = c.DependencyCount
            };
        }).OrderByDescending(x => x.IDI));
    }
}
