using Microsoft.AspNetCore.Mvc;
using SynapsePlatform.Api.DTOs;
using SynapsePlatform.Core.Interfaces;

namespace SynapsePlatform.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class IDIController : ControllerBase
{
    private readonly IIDIService _idiService;

    public IDIController(IIDIService idiService)
    {
        _idiService = idiService;
    }

    [HttpGet("project/{projectId}")]
    public async Task<ActionResult<IDIReportDto>> GetProjectIDI(Guid projectId)
    {
        var report = await _idiService.GetIDIReportAsync(projectId);

        return Ok(new IDIReportDto(
            report.ProjectIDI,
            report.Status,
            report.Components.Select(c => new ComponentIDIDto(
                c.ComponentId, c.ComponentName, c.IDI, c.Status, c.DaysSinceLastIntegration
            )),
            report.Trends.Select(t => new IDITrendDto(t.Date, t.IDI))
        ));
    }

    [HttpPost("component/{componentId}/calculate")]
    public async Task<IActionResult> RecalculateComponentIDI(Guid componentId)
    {
        await _idiService.UpdateComponentIDIAsync(componentId);
        return NoContent();
    }
}
