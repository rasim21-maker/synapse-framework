using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;
using SynapsePlatform.Core.Entities;

namespace SynapsePlatform.Infrastructure.Data;

public class SynapseDbContext : IdentityDbContext<ApplicationUser, Microsoft.AspNetCore.Identity.IdentityRole<Guid>, Guid>
{
    public SynapseDbContext(DbContextOptions<SynapseDbContext> options) : base(options) { }

    public DbSet<Organization> Organizations => Set<Organization>();
    public DbSet<Portfolio> Portfolios => Set<Portfolio>();
    public DbSet<Project> Projects => Set<Project>();
    public DbSet<Component> Components => Set<Component>();
    public DbSet<Sprint> Sprints => Set<Sprint>();
    public DbSet<WorkItem> WorkItems => Set<WorkItem>();
    public DbSet<DigitalTwin> DigitalTwins => Set<DigitalTwin>();
    public DbSet<QualityGate> QualityGates => Set<QualityGate>();
    public DbSet<QualityGateResult> QualityGateResults => Set<QualityGateResult>();
    public DbSet<IntegrationRecord> IntegrationRecords => Set<IntegrationRecord>();
    public DbSet<Team> Teams => Set<Team>();
    public DbSet<Risk> Risks => Set<Risk>();
    public DbSet<Comment> Comments => Set<Comment>();
    public DbSet<Attachment> Attachments => Set<Attachment>();
    public DbSet<WorkItemHistory> WorkItemHistories => Set<WorkItemHistory>();
    public DbSet<Checklist> Checklists => Set<Checklist>();
    public DbSet<ChecklistItem> ChecklistItems => Set<ChecklistItem>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        modelBuilder.Entity<Organization>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.HasQueryFilter(e => !e.IsDeleted);
        });

        modelBuilder.Entity<Project>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.HasIndex(e => e.Code).IsUnique();
            entity.HasQueryFilter(e => !e.IsDeleted);
            entity.HasOne(e => e.Portfolio).WithMany(p => p.Projects).HasForeignKey(e => e.PortfolioId);
            entity.HasOne(e => e.ProjectManager).WithMany().HasForeignKey(e => e.ProjectManagerId);
        });

        modelBuilder.Entity<Component>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.HasQueryFilter(e => !e.IsDeleted);
            entity.HasOne(e => e.Project).WithMany(p => p.Components).HasForeignKey(e => e.ProjectId);
            entity.HasOne(e => e.DigitalTwin).WithMany(d => d.Components).HasForeignKey(e => e.DigitalTwinId);
        });

        modelBuilder.Entity<WorkItem>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.HasQueryFilter(e => !e.IsDeleted);
            entity.HasOne(e => e.Project).WithMany(p => p.WorkItems).HasForeignKey(e => e.ProjectId);
            entity.HasOne(e => e.Sprint).WithMany(s => s.WorkItems).HasForeignKey(e => e.SprintId);
            entity.HasOne(e => e.ParentWorkItem).WithMany(w => w.ChildWorkItems).HasForeignKey(e => e.ParentWorkItemId);
        });

        modelBuilder.Entity<Sprint>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.HasQueryFilter(e => !e.IsDeleted);
            entity.HasOne(e => e.Project).WithMany(p => p.Sprints).HasForeignKey(e => e.ProjectId);
        });

        modelBuilder.Entity<QualityGate>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.HasQueryFilter(e => !e.IsDeleted);
            entity.HasOne(e => e.Project).WithMany(p => p.QualityGates).HasForeignKey(e => e.ProjectId);
        });
    }
}
