using SynapsePlatform.Core.Enums;

namespace SynapsePlatform.Core.Entities;

public class Project : BaseEntity
{
    public string Name { get; set; } = string.Empty;
    public string Code { get; set; } = string.Empty;
    public string? Description { get; set; }
    public ProjectArchetype Archetype { get; set; }
    public ProjectPhase CurrentPhase { get; set; } = ProjectPhase.Initiation;
    public MaturityLevel TargetMaturityLevel { get; set; } = MaturityLevel.Level1_Instrumented;

    public DateTime PlannedStartDate { get; set; }
    public DateTime PlannedEndDate { get; set; }
    public DateTime? ActualStartDate { get; set; }
    public DateTime? ActualEndDate { get; set; }

    public double CurrentIDI { get; set; }
    public IDIStatus IDIStatus { get; set; } = IDIStatus.Healthy;
    public double IDIThreshold { get; set; } = 5.0;

    public double PlannedBudget { get; set; }
    public double ActualBudget { get; set; }

    public Guid? PortfolioId { get; set; }
    public Guid? ProjectManagerId { get; set; }

    public virtual Portfolio? Portfolio { get; set; }
    public virtual ApplicationUser? ProjectManager { get; set; }
    public virtual ICollection<Component> Components { get; set; } = new List<Component>();
    public virtual ICollection<Sprint> Sprints { get; set; } = new List<Sprint>();
    public virtual ICollection<WorkItem> WorkItems { get; set; } = new List<WorkItem>();
    public virtual ICollection<QualityGate> QualityGates { get; set; } = new List<QualityGate>();
    public virtual ICollection<Risk> Risks { get; set; } = new List<Risk>();
    public virtual ICollection<Team> Teams { get; set; } = new List<Team>();
}
