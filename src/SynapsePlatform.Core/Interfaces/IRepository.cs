using System.Linq.Expressions;
using SynapsePlatform.Core.Entities;

namespace SynapsePlatform.Core.Interfaces;

public interface IRepository<T> where T : BaseEntity
{
    Task<T?> GetByIdAsync(Guid id);
    Task<IEnumerable<T>> GetAllAsync();
    Task<IEnumerable<T>> FindAsync(Expression<Func<T, bool>> predicate);
    Task<T> AddAsync(T entity);
    Task UpdateAsync(T entity);
    Task DeleteAsync(Guid id);
    Task<bool> ExistsAsync(Guid id);
    IQueryable<T> Query();
}

public interface IUnitOfWork : IDisposable
{
    IRepository<Organization> Organizations { get; }
    IRepository<Portfolio> Portfolios { get; }
    IRepository<Project> Projects { get; }
    IRepository<Component> Components { get; }
    IRepository<Sprint> Sprints { get; }
    IRepository<WorkItem> WorkItems { get; }
    IRepository<DigitalTwin> DigitalTwins { get; }
    IRepository<QualityGate> QualityGates { get; }
    IRepository<IntegrationRecord> IntegrationRecords { get; }
    IRepository<Team> Teams { get; }
    IRepository<ApplicationUser> Users { get; }
    IRepository<Risk> Risks { get; }
    IRepository<Comment> Comments { get; }
    Task<int> SaveChangesAsync();
}
