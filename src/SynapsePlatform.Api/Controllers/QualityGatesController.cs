using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using SynapsePlatform.Api.DTOs;
using SynapsePlatform.Core.Entities;
using SynapsePlatform.Core.Interfaces;
using SynapsePlatform.Infrastructure.Data;

namespace SynapsePlatform.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class QualityGatesController : ControllerBase
{
    private readonly IQualityGateService _qualityGateService;
    private readonly SynapseDbContext _context;

    public QualityGatesController(IQualityGateService qualityGateService, SynapseDbContext context)
    {
        _qualityGateService = qualityGateService;
        _context = context;
    }

    [HttpGet]
    public async Task<ActionResult<IEnumerable<QualityGateDto>>> GetQualityGates([FromQuery] Guid projectId)
    {
        var gates = await _context.QualityGates
            .Where(g => g.ProjectId == projectId)
            .ToListAsync();

        return Ok(gates.Select(g => new QualityGateDto(
            g.Id,
            g.Name,
            g.Description,
            g.Category,
            g.ThresholdValue,
            g.ThresholdUnit,
            g.Enforcement,
            g.Action,
            g.IsEnabled,
            g.LastCheckPassed,
            g.LastCheckedAt
        )));
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<QualityGateDto>> GetQualityGate(Guid id)
    {
        var gate = await _context.QualityGates.FindAsync(id);
        if (gate == null)
            return NotFound();

        return Ok(new QualityGateDto(
            gate.Id,
            gate.Name,
            gate.Description,
            gate.Category,
            gate.ThresholdValue,
            gate.ThresholdUnit,
            gate.Enforcement,
            gate.Action,
            gate.IsEnabled,
            gate.LastCheckPassed,
            gate.LastCheckedAt
        ));
    }

    [HttpPost]
    public async Task<ActionResult<QualityGateDto>> CreateQualityGate(CreateQualityGateDto dto)
    {
        var gate = new QualityGate
        {
            Name = dto.Name,
            Description = dto.Description,
            Category = dto.Category,
            ThresholdValue = dto.ThresholdValue,
            ThresholdUnit = dto.ThresholdUnit,
            ThresholdOperator = dto.ThresholdOperator,
            Enforcement = dto.Enforcement,
            Action = dto.Action,
            PolicyYaml = dto.PolicyYaml,
            ProjectId = dto.ProjectId,
            ComponentId = dto.ComponentId
        };

        var created = await _qualityGateService.CreateQualityGateAsync(gate);

        return CreatedAtAction(nameof(GetQualityGate), new { id = created.Id }, new QualityGateDto(
            created.Id,
            created.Name,
            created.Description,
            created.Category,
            created.ThresholdValue,
            created.ThresholdUnit,
            created.Enforcement,
            created.Action,
            created.IsEnabled,
            created.LastCheckPassed,
            created.LastCheckedAt
        ));
    }

    [HttpPost("{id}/check")]
    public async Task<ActionResult<object>> CheckQualityGate(Guid id, [FromBody] double actualValue)
    {
        var result = await _qualityGateService.CheckQualityGateAsync(id, actualValue);

        return Ok(new
        {
            result.Passed,
            result.ActualValue,
            result.Message,
            result.CheckedAt
        });
    }

    [HttpPost("project/{projectId}/check-all")]
    public async Task<ActionResult<IEnumerable<object>>> CheckAllGates(Guid projectId)
    {
        var results = await _qualityGateService.CheckAllProjectGatesAsync(projectId);

        return Ok(results.Select(r => new
        {
            r.QualityGateId,
            r.Passed,
            r.ActualValue,
            r.Message,
            r.CheckedAt
        }));
    }

    [HttpGet("project/{projectId}/can-commit")]
    public async Task<ActionResult<object>> CanCommit(Guid projectId, [FromQuery] string commitHash)
    {
        var canProceed = await _qualityGateService.CanProceedWithCommit(projectId, commitHash);
        return Ok(new { CanCommit = canProceed, CommitHash = commitHash });
    }

    [HttpGet("project/{projectId}/can-deploy")]
    public async Task<ActionResult<object>> CanDeploy(Guid projectId)
    {
        var canProceed = await _qualityGateService.CanProceedWithDeployment(projectId);
        return Ok(new { CanDeploy = canProceed });
    }

    [HttpPatch("{id}/toggle")]
    public async Task<IActionResult> ToggleQualityGate(Guid id)
    {
        var gate = await _context.QualityGates.FindAsync(id);
        if (gate == null)
            return NotFound();

        gate.IsEnabled = !gate.IsEnabled;
        gate.UpdatedAt = DateTime.UtcNow;
        await _context.SaveChangesAsync();

        return NoContent();
    }
}
