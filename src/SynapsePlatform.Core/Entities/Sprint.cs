namespace SynapsePlatform.Core.Entities;

public class Sprint : BaseEntity
{
    public string Name { get; set; } = string.Empty;
    public string? Goal { get; set; }
    public int SprintNumber { get; set; }
    public DateTime StartDate { get; set; }
    public DateTime EndDate { get; set; }
    public bool IsActive { get; set; } = false;
    public bool IsCompleted { get; set; } = false;

    public int PlannedStoryPoints { get; set; }
    public int CompletedStoryPoints { get; set; }
    public double? PlannedCapacityHours { get; set; }

    public string? WhatWentWell { get; set; }
    public string? WhatToImprove { get; set; }

    public Guid ProjectId { get; set; }
    public virtual Project? Project { get; set; }
    public virtual ICollection<WorkItem> WorkItems { get; set; } = new List<WorkItem>();
}

public class SprintMetrics
{
    public int PlannedStoryPoints { get; set; }
    public int CompletedStoryPoints { get; set; }
    public double Velocity { get; set; }
    public int TotalTasks { get; set; }
    public int CompletedTasks { get; set; }
    public int RemainingTasks { get; set; }
    public double BurndownRate { get; set; }
}
