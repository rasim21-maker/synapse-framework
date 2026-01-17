using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using SynapsePlatform.Api.DTOs;
using SynapsePlatform.Core.Entities;
using SynapsePlatform.Core.Interfaces;
using SynapsePlatform.Infrastructure.Data;

namespace SynapsePlatform.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class ProjectsController : ControllerBase
{
    private readonly SynapseDbContext _context;
    private readonly IIDIService _idiService;

    public ProjectsController(SynapseDbContext context, IIDIService idiService)
    {
        _context = context;
        _idiService = idiService;
    }

    [HttpGet]
    public async Task<ActionResult<IEnumerable<ProjectDto>>> GetProjects([FromQuery] Guid? portfolioId)
    {
        var query = _context.Projects
            .Include(p => p.Components)
            .Include(p => p.WorkItems)
            .Include(p => p.ProjectManager)
            .AsQueryable();

        if (portfolioId.HasValue)
            query = query.Where(p => p.PortfolioId == portfolioId);

        var projects = await query.ToListAsync();

        return Ok(projects.Select(p => new ProjectDto(
            p.Id, p.Name, p.Code, p.Description, p.Archetype, p.CurrentPhase,
            p.TargetMaturityLevel, p.PlannedStartDate, p.PlannedEndDate,
            p.CurrentIDI, p.IDIStatus, p.PlannedBudget, p.ActualBudget,
            p.ProjectManager?.FullName, p.Components.Count, p.WorkItems.Count
        )));
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<ProjectDto>> GetProject(Guid id)
    {
        var project = await _context.Projects
            .Include(p => p.Components)
            .Include(p => p.WorkItems)
            .Include(p => p.ProjectManager)
            .FirstOrDefaultAsync(p => p.Id == id);

        if (project == null) return NotFound();

        return Ok(new ProjectDto(
            project.Id, project.Name, project.Code, project.Description,
            project.Archetype, project.CurrentPhase, project.TargetMaturityLevel,
            project.PlannedStartDate, project.PlannedEndDate, project.CurrentIDI,
            project.IDIStatus, project.PlannedBudget, project.ActualBudget,
            project.ProjectManager?.FullName, project.Components.Count, project.WorkItems.Count
        ));
    }

    [HttpGet("{id}/dashboard")]
    public async Task<ActionResult<object>> GetProjectDashboard(Guid id)
    {
        var project = await _context.Projects
            .Include(p => p.Components)
            .Include(p => p.WorkItems)
            .Include(p => p.Sprints)
            .Include(p => p.Risks)
            .FirstOrDefaultAsync(p => p.Id == id);

        if (project == null) return NotFound();

        var idiReport = await _idiService.GetIDIReportAsync(id);
        var activeSprint = project.Sprints.FirstOrDefault(s => s.IsActive);

        return Ok(new
        {
            Project = new ProjectDto(
                project.Id, project.Name, project.Code, project.Description,
                project.Archetype, project.CurrentPhase, project.TargetMaturityLevel,
                project.PlannedStartDate, project.PlannedEndDate, project.CurrentIDI,
                project.IDIStatus, project.PlannedBudget, project.ActualBudget,
                null, project.Components.Count, project.WorkItems.Count
            ),
            ActiveSprint = activeSprint != null ? new SprintDto(
                activeSprint.Id, activeSprint.Name, activeSprint.Goal,
                activeSprint.SprintNumber, activeSprint.StartDate, activeSprint.EndDate,
                activeSprint.IsActive, activeSprint.IsCompleted,
                activeSprint.PlannedStoryPoints, activeSprint.CompletedStoryPoints,
                activeSprint.WorkItems?.Count ?? 0
            ) : null,
            IDIReport = new IDIReportDto(
                idiReport.ProjectIDI, idiReport.Status,
                idiReport.Components.Select(c => new ComponentIDIDto(
                    c.ComponentId, c.ComponentName, c.IDI, c.Status, c.DaysSinceLastIntegration
                )),
                idiReport.Trends.Select(t => new IDITrendDto(t.Date, t.IDI))
            ),
            OpenWorkItems = project.WorkItems.Count(w => w.Status != Core.Enums.WorkItemStatus.Done),
            CompletedWorkItems = project.WorkItems.Count(w => w.Status == Core.Enums.WorkItemStatus.Done),
            BlockedWorkItems = project.WorkItems.Count(w => w.Status == Core.Enums.WorkItemStatus.Blocked),
            OpenRisks = project.Risks.Count(r => r.Status != Core.Enums.RiskStatus.Resolved),
            BudgetUtilization = project.PlannedBudget > 0 ? (project.ActualBudget / project.PlannedBudget) * 100 : 0
        });
    }

    [HttpPost]
    public async Task<ActionResult<ProjectDto>> CreateProject(CreateProjectDto dto)
    {
        var project = new Project
        {
            Name = dto.Name,
            Code = dto.Code,
            Description = dto.Description,
            Archetype = dto.Archetype,
            TargetMaturityLevel = dto.TargetMaturityLevel,
            PlannedStartDate = dto.PlannedStartDate,
            PlannedEndDate = dto.PlannedEndDate,
            PlannedBudget = dto.PlannedBudget,
            PortfolioId = dto.PortfolioId,
            ProjectManagerId = dto.ProjectManagerId
        };

        _context.Projects.Add(project);
        await _context.SaveChangesAsync();

        return CreatedAtAction(nameof(GetProject), new { id = project.Id }, new ProjectDto(
            project.Id, project.Name, project.Code, project.Description,
            project.Archetype, project.CurrentPhase, project.TargetMaturityLevel,
            project.PlannedStartDate, project.PlannedEndDate, 0, Core.Enums.IDIStatus.Healthy,
            project.PlannedBudget, 0, null, 0, 0
        ));
    }

    [HttpPut("{id}/phase")]
    public async Task<IActionResult> UpdatePhase(Guid id, [FromBody] Core.Enums.ProjectPhase newPhase)
    {
        var project = await _context.Projects.FindAsync(id);
        if (project == null) return NotFound();

        project.CurrentPhase = newPhase;
        project.UpdatedAt = DateTime.UtcNow;
        await _context.SaveChangesAsync();

        return NoContent();
    }
}
