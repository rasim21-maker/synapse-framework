FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
WORKDIR /app
EXPOSE 8080

FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY ["src/SynapsePlatform.Api/SynapsePlatform.Api.csproj", "SynapsePlatform.Api/"]
COPY ["src/SynapsePlatform.Core/SynapsePlatform.Core.csproj", "SynapsePlatform.Core/"]
COPY ["src/SynapsePlatform.Infrastructure/SynapsePlatform.Infrastructure.csproj", "SynapsePlatform.Infrastructure/"]
RUN dotnet restore "SynapsePlatform.Api/SynapsePlatform.Api.csproj"
COPY src/ .
WORKDIR "/src/SynapsePlatform.Api"
RUN dotnet build "SynapsePlatform.Api.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "SynapsePlatform.Api.csproj" -c Release -o /app/publish /p:UseAppHost=false

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "SynapsePlatform.Api.dll"]
