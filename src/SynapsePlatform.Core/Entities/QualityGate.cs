using SynapsePlatform.Core.Enums;

namespace SynapsePlatform.Core.Entities;

public class QualityGate : BaseEntity
{
    public string Name { get; set; } = string.Empty;
    public string? Description { get; set; }
    public string MetricName { get; set; } = string.Empty;
    public double ThresholdValue { get; set; }
    public string? ThresholdUnit { get; set; }
    public QualityGateEnforcement Enforcement { get; set; }
    public QualityGateAction Action { get; set; }
    public bool IsActive { get; set; } = true;
    public string? PolicyCode { get; set; }

    public Guid ProjectId { get; set; }
    public Guid? ComponentId { get; set; }
    public virtual Project? Project { get; set; }
    public virtual Component? Component { get; set; }
    public virtual ICollection<QualityGateResult> Results { get; set; } = new List<QualityGateResult>();
}

public class QualityGateResult : BaseEntity
{
    public bool Passed { get; set; }
    public double ActualValue { get; set; }
    public string? Message { get; set; }
    public DateTime EvaluatedAt { get; set; } = DateTime.UtcNow;

    public Guid QualityGateId { get; set; }
    public virtual QualityGate? QualityGate { get; set; }
}
