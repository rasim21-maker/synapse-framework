using Microsoft.EntityFrameworkCore;
using SynapsePlatform.Core.Entities;
using SynapsePlatform.Core.Enums;
using SynapsePlatform.Core.Interfaces;
using SynapsePlatform.Infrastructure.Data;

namespace SynapsePlatform.Infrastructure.Services;

public class SprintService : ISprintService
{
    private readonly SynapseDbContext _context;

    public SprintService(SynapseDbContext context)
    {
        _context = context;
    }

    public async Task<Sprint> CreateSprintAsync(Sprint sprint)
    {
        // Auto-generate sprint number
        var existingCount = await _context.Sprints
            .CountAsync(s => s.ProjectId == sprint.ProjectId);
        sprint.SprintNumber = existingCount + 1;

        if (string.IsNullOrEmpty(sprint.Name))
        {
            sprint.Name = $"Sprint {sprint.SprintNumber}";
        }

        _context.Sprints.Add(sprint);
        await _context.SaveChangesAsync();
        return sprint;
    }

    public async Task<Sprint?> GetActiveSprintAsync(Guid projectId)
    {
        return await _context.Sprints
            .Where(s => s.ProjectId == projectId && s.IsActive)
            .Include(s => s.WorkItems)
                .ThenInclude(w => w.Assignee)
            .FirstOrDefaultAsync();
    }

    public async Task<IEnumerable<Sprint>> GetSprintsByProjectAsync(Guid projectId)
    {
        return await _context.Sprints
            .Where(s => s.ProjectId == projectId)
            .OrderByDescending(s => s.SprintNumber)
            .ToListAsync();
    }

    public async Task StartSprintAsync(Guid sprintId)
    {
        var sprint = await _context.Sprints.FindAsync(sprintId);
        if (sprint == null)
            throw new ArgumentException("Sprint not found", nameof(sprintId));

        // Close any currently active sprint
        var activeSprint = await _context.Sprints
            .FirstOrDefaultAsync(s => s.ProjectId == sprint.ProjectId && s.IsActive);

        if (activeSprint != null && activeSprint.Id != sprintId)
        {
            activeSprint.IsActive = false;
        }

        sprint.IsActive = true;
        sprint.StartDate = DateTime.UtcNow;

        // Calculate planned story points from work items
        var workItems = await _context.WorkItems
            .Where(w => w.SprintId == sprintId)
            .ToListAsync();

        sprint.PlannedStoryPoints = workItems.Sum(w => w.StoryPoints ?? 0);

        await _context.SaveChangesAsync();
    }

    public async Task CompleteSprintAsync(Guid sprintId, string? whatWentWell, string? whatToImprove)
    {
        var sprint = await _context.Sprints
            .Include(s => s.WorkItems)
            .FirstOrDefaultAsync(s => s.Id == sprintId);

        if (sprint == null)
            throw new ArgumentException("Sprint not found", nameof(sprintId));

        sprint.IsActive = false;
        sprint.IsCompleted = true;
        sprint.EndDate = DateTime.UtcNow;
        sprint.WhatWentWell = whatWentWell;
        sprint.WhatToImprove = whatToImprove;

        // Calculate completed story points
        sprint.CompletedStoryPoints = sprint.WorkItems
            .Where(w => w.Status == WorkItemStatus.Done)
            .Sum(w => w.StoryPoints ?? 0);

        await _context.SaveChangesAsync();
    }

    public async Task<SprintMetrics> GetSprintMetricsAsync(Guid sprintId)
    {
        var sprint = await _context.Sprints
            .Include(s => s.WorkItems)
            .FirstOrDefaultAsync(s => s.Id == sprintId);

        if (sprint == null)
            throw new ArgumentException("Sprint not found", nameof(sprintId));

        var completedItems = sprint.WorkItems.Where(w => w.Status == WorkItemStatus.Done).ToList();
        var remainingItems = sprint.WorkItems.Where(w => w.Status != WorkItemStatus.Done).ToList();

        var totalDays = (sprint.EndDate - sprint.StartDate).Days;
        var elapsedDays = Math.Max(1, (DateTime.UtcNow - sprint.StartDate).Days);

        return new SprintMetrics
        {
            PlannedStoryPoints = sprint.PlannedStoryPoints,
            CompletedStoryPoints = completedItems.Sum(w => w.StoryPoints ?? 0),
            Velocity = totalDays > 0 ? sprint.CompletedStoryPoints / (double)totalDays : 0,
            TotalTasks = sprint.WorkItems.Count,
            CompletedTasks = completedItems.Count,
            RemainingTasks = remainingItems.Count,
            BurndownRate = totalDays > 0 && sprint.PlannedStoryPoints > 0
                ? (sprint.PlannedStoryPoints - completedItems.Sum(w => w.StoryPoints ?? 0)) / (double)(totalDays - elapsedDays + 1)
                : 0
        };
    }
}
