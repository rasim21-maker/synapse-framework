using Microsoft.AspNetCore.Mvc;
using SynapsePlatform.Api.DTOs;
using SynapsePlatform.Core.Entities;
using SynapsePlatform.Core.Interfaces;

namespace SynapsePlatform.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class SprintsController : ControllerBase
{
    private readonly ISprintService _sprintService;

    public SprintsController(ISprintService sprintService)
    {
        _sprintService = sprintService;
    }

    [HttpGet]
    public async Task<ActionResult<IEnumerable<SprintDto>>> GetSprints([FromQuery] Guid projectId)
    {
        var sprints = await _sprintService.GetSprintsByProjectAsync(projectId);

        return Ok(sprints.Select(s => new SprintDto(
            s.Id,
            s.Name,
            s.Goal,
            s.SprintNumber,
            s.StartDate,
            s.EndDate,
            s.IsActive,
            s.IsCompleted,
            s.PlannedStoryPoints,
            s.CompletedStoryPoints,
            s.WorkItems?.Count ?? 0
        )));
    }

    [HttpGet("active")]
    public async Task<ActionResult<SprintDto>> GetActiveSprint([FromQuery] Guid projectId)
    {
        var sprint = await _sprintService.GetActiveSprintAsync(projectId);
        if (sprint == null)
            return NotFound("No active sprint found");

        return Ok(new SprintDto(
            sprint.Id,
            sprint.Name,
            sprint.Goal,
            sprint.SprintNumber,
            sprint.StartDate,
            sprint.EndDate,
            sprint.IsActive,
            sprint.IsCompleted,
            sprint.PlannedStoryPoints,
            sprint.CompletedStoryPoints,
            sprint.WorkItems?.Count ?? 0
        ));
    }

    [HttpGet("{id}/metrics")]
    public async Task<ActionResult<SprintMetrics>> GetSprintMetrics(Guid id)
    {
        var metrics = await _sprintService.GetSprintMetricsAsync(id);
        return Ok(metrics);
    }

    [HttpPost]
    public async Task<ActionResult<SprintDto>> CreateSprint(CreateSprintDto dto)
    {
        var sprint = new Sprint
        {
            Name = dto.Name ?? "",
            Goal = dto.Goal,
            StartDate = dto.StartDate,
            EndDate = dto.EndDate,
            PlannedCapacityHours = dto.PlannedCapacityHours,
            ProjectId = dto.ProjectId
        };

        var created = await _sprintService.CreateSprintAsync(sprint);

        return CreatedAtAction(nameof(GetSprints), new { projectId = dto.ProjectId }, new SprintDto(
            created.Id,
            created.Name,
            created.Goal,
            created.SprintNumber,
            created.StartDate,
            created.EndDate,
            created.IsActive,
            created.IsCompleted,
            created.PlannedStoryPoints,
            created.CompletedStoryPoints,
            0
        ));
    }

    [HttpPost("{id}/start")]
    public async Task<IActionResult> StartSprint(Guid id)
    {
        await _sprintService.StartSprintAsync(id);
        return NoContent();
    }

    [HttpPost("{id}/complete")]
    public async Task<IActionResult> CompleteSprint(Guid id, [FromBody] CompleteSprintRequest request)
    {
        await _sprintService.CompleteSprintAsync(id, request.WhatWentWell, request.WhatToImprove);
        return NoContent();
    }
}

public record CompleteSprintRequest(string? WhatWentWell, string? WhatToImprove);
