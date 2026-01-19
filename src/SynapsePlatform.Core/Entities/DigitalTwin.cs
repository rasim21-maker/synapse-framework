using SynapsePlatform.Core.Enums;

namespace SynapsePlatform.Core.Entities;

public class DigitalTwin : BaseEntity
{
    public string Name { get; set; } = string.Empty;
    public string? Description { get; set; }
    public DigitalTwinLayer Layer { get; set; }
    public string? SimulationEngineType { get; set; }
    public string? ConfigurationPath { get; set; }
    public double SimToRealityAccuracy { get; set; }
    public bool IsActive { get; set; } = true;
    public DateTime? LastSyncDate { get; set; }

    public Guid ProjectId { get; set; }
    public virtual Project? Project { get; set; }
    public virtual ICollection<Component> Components { get; set; } = new List<Component>();
}
