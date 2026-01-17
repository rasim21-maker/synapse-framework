using SynapsePlatform.Core.Enums;

namespace SynapsePlatform.Core.Entities;

/// <summary>
/// Represents a system component (hardware, firmware, software, infrastructure)
/// </summary>
public class Component : BaseEntity
{
    public string Name { get; set; } = string.Empty;
    public string? Description { get; set; }
    public string? Version { get; set; }
    public ComponentType Type { get; set; }
    public string? RepositoryUrl { get; set; }

    // Integration status
    public bool IsIntegrated { get; set; } = false;
    public DateTime? LastIntegrationDate { get; set; }
    public int LinesOfCodeChanged { get; set; }
    public int DaysSinceLastIntegration { get; set; }

    // Dependencies count for IDI calculation
    public int DependencyCount { get; set; }

    // Calculated IDI for this component
    // IDI = (Days Since Last Integration) × (LoC Changed / 1000) × (Dependencies / 10)
    public double ComponentIDI { get; set; }

    // Hardware specific properties
    public double? PowerBudgetWatts { get; set; }
    public double? ActualPowerWatts { get; set; }
    public double? ThermalLimitCelsius { get; set; }
    public double? ActualThermalCelsius { get; set; }

    // Software specific properties
    public double? LatencyThresholdMs { get; set; }
    public double? ActualLatencyMs { get; set; }
    public double? MemoryLimitMB { get; set; }
    public double? ActualMemoryMB { get; set; }

    // Foreign keys
    public Guid ProjectId { get; set; }
    public Guid? DigitalTwinId { get; set; }
    public Guid? OwnerTeamId { get; set; }

    // Navigation properties
    public virtual Project? Project { get; set; }
    public virtual DigitalTwin? DigitalTwin { get; set; }
    public virtual Team? OwnerTeam { get; set; }
    public virtual ICollection<Component> Dependencies { get; set; } = new List<Component>();
    public virtual ICollection<Component> Dependents { get; set; } = new List<Component>();
    public virtual ICollection<WorkItem> WorkItems { get; set; } = new List<WorkItem>();
}
