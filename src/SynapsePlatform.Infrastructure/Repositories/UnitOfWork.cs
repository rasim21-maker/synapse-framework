using SynapsePlatform.Core.Entities;
using SynapsePlatform.Core.Interfaces;
using SynapsePlatform.Infrastructure.Data;

namespace SynapsePlatform.Infrastructure.Repositories;

public class UnitOfWork : IUnitOfWork
{
    private readonly SynapseDbContext _context;
    private bool _disposed = false;

    private IRepository<Organization>? _organizations;
    private IRepository<Portfolio>? _portfolios;
    private IRepository<Project>? _projects;
    private IRepository<Component>? _components;
    private IRepository<Sprint>? _sprints;
    private IRepository<WorkItem>? _workItems;
    private IRepository<DigitalTwin>? _digitalTwins;
    private IRepository<QualityGate>? _qualityGates;
    private IRepository<IntegrationRecord>? _integrationRecords;
    private IRepository<Team>? _teams;
    private IRepository<ApplicationUser>? _users;
    private IRepository<Risk>? _risks;
    private IRepository<Comment>? _comments;

    public UnitOfWork(SynapseDbContext context)
    {
        _context = context;
    }

    public IRepository<Organization> Organizations =>
        _organizations ??= new Repository<Organization>(_context);

    public IRepository<Portfolio> Portfolios =>
        _portfolios ??= new Repository<Portfolio>(_context);

    public IRepository<Project> Projects =>
        _projects ??= new Repository<Project>(_context);

    public IRepository<Component> Components =>
        _components ??= new Repository<Component>(_context);

    public IRepository<Sprint> Sprints =>
        _sprints ??= new Repository<Sprint>(_context);

    public IRepository<WorkItem> WorkItems =>
        _workItems ??= new Repository<WorkItem>(_context);

    public IRepository<DigitalTwin> DigitalTwins =>
        _digitalTwins ??= new Repository<DigitalTwin>(_context);

    public IRepository<QualityGate> QualityGates =>
        _qualityGates ??= new Repository<QualityGate>(_context);

    public IRepository<IntegrationRecord> IntegrationRecords =>
        _integrationRecords ??= new Repository<IntegrationRecord>(_context);

    public IRepository<Team> Teams =>
        _teams ??= new Repository<Team>(_context);

    public IRepository<ApplicationUser> Users =>
        _users ??= new Repository<ApplicationUser>(_context);

    public IRepository<Risk> Risks =>
        _risks ??= new Repository<Risk>(_context);

    public IRepository<Comment> Comments =>
        _comments ??= new Repository<Comment>(_context);

    public async Task<int> SaveChangesAsync()
    {
        return await _context.SaveChangesAsync();
    }

    protected virtual void Dispose(bool disposing)
    {
        if (!_disposed && disposing)
        {
            _context.Dispose();
        }
        _disposed = true;
    }

    public void Dispose()
    {
        Dispose(true);
        GC.SuppressFinalize(this);
    }
}
