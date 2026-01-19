using SynapsePlatform.Core.Enums;

namespace SynapsePlatform.Core.Entities;

public class IntegrationRecord : BaseEntity
{
    public DateTime IntegrationDate { get; set; } = DateTime.UtcNow;
    public bool WasSuccessful { get; set; }
    public double IDIBeforeIntegration { get; set; }
    public double IDIAfterIntegration { get; set; }
    public int LinesOfCodeIntegrated { get; set; }
    public int IssuesFound { get; set; }
    public int IssuesResolved { get; set; }
    public string? Notes { get; set; }
    public TimeSpan Duration { get; set; }

    public Guid ProjectId { get; set; }
    public Guid? ComponentId { get; set; }
    public Guid? PerformedById { get; set; }

    public virtual Project? Project { get; set; }
    public virtual Component? Component { get; set; }
    public virtual ApplicationUser? PerformedBy { get; set; }
}
