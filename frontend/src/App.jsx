import { useEffect, useState } from "react"

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts"

import "./App.css"


const API = "http://127.0.0.1:8000"


const QUERY_TYPES = [
  "Temporal",
  "Spatial",
  "Spatio-temporal",
  "Temporal + Attribute",
  "Spatial + Attribute",
  "Spatio-temporal + Attribute",
]


const TABS = [
  { id: "overview", label: "Overview" },
  { id: "router", label: "Live Router" },
  { id: "performance", label: "Performance" },
  { id: "routing", label: "Routing Analysis" },
  { id: "query", label: "Query Analysis" },
  { id: "indexes", label: "Indexes" },
]


const INDEX_LABELS = {
  pickup_time_1: "Temporal Index",
  pickup_location_2dsphere: "Spatial Index",
  pickup_location_2dsphere_pickup_time_1: "Compound Index",
}


const PIE_COLORS = [
  "#2563eb",
  "#16a34a",
  "#9333ea",
]


/* =========================================================
   QUERY-TYPE CHART COLORS
   Only used in Query-Type Analysis
   ========================================================= */

const QUERY_CHART_COLORS = [
  "#3B82F6",
  "#10B981",
  "#F59E0B",
  "#EF4444",
  "#8B5CF6",
  "#06B6D4",
]


function formatMs(value) {
  if (value === undefined || value === null) {
    return "—"
  }

  return `${Number(value).toFixed(2)} ms`
}


function formatPercent(value) {
  if (value === undefined || value === null) {
    return "—"
  }

  return `${Number(value).toFixed(2)}%`
}


function formatNumber(value) {
  if (value === undefined || value === null) {
    return "—"
  }

  return Number(value).toLocaleString()
}


function downloadTextFile(filename, content, mimeType = "text/plain;charset=utf-8") {
  const blob = new Blob([content], { type: mimeType })
  const url = URL.createObjectURL(blob)
  const link = document.createElement("a")
  link.href = url
  link.download = filename
  document.body.appendChild(link)
  link.click()
  link.remove()
  URL.revokeObjectURL(url)
}


function App() {

  const [activeTab, setActiveTab] =
    useState("overview")

  const [health, setHealth] =
    useState(null)

  const [analytics, setAnalytics] =
    useState(null)

  const [selectedQuery, setSelectedQuery] =
    useState("Temporal")

  const [routeResult, setRouteResult] =
    useState(null)

  const [executeResult, setExecuteResult] =
    useState(null)

  const [routing, setRouting] =
    useState(false)

  const [executing, setExecuting] =
    useState(false)

  const [error, setError] =
    useState("")


  useEffect(() => {
    loadDashboard()
  }, [])


  async function loadDashboard() {

    try {

      setError("")

      const healthResponse =
        await fetch(`${API}/api/health`)

      const healthData =
        await healthResponse.json()

      setHealth(healthData)

      const analyticsResponse =
        await fetch(`${API}/api/analytics`)

      const analyticsData =
        await analyticsResponse.json()

      setAnalytics(analyticsData)

    } catch (err) {

      console.error(err)

      setError(
        "Unable to connect to backend. Make sure FastAPI is running on port 8000."
      )

    }
  }


  async function routeQuery() {

    try {

      setRouting(true)
      setError("")
      setRouteResult(null)

      const response =
        await fetch(
          `${API}/api/route?query_type=${encodeURIComponent(
            selectedQuery
          )}`,
          {
            method: "POST",
          }
        )

      if (!response.ok) {
        throw new Error("Routing failed")
      }

      const data =
        await response.json()

      setRouteResult(data)

    } catch (err) {

      console.error(err)

      setError(
        "Unable to route the query."
      )

    } finally {

      setRouting(false)

    }
  }


  async function executeQuery() {

    try {

      setExecuting(true)
      setError("")
      setExecuteResult(null)

      const response =
        await fetch(
          `${API}/api/execute?query_type=${encodeURIComponent(
            selectedQuery
          )}`,
          {
            method: "POST",
          }
        )

      if (!response.ok) {
        throw new Error("Execution failed")
      }

      const data =
        await response.json()

      setExecuteResult(data)

    } catch (err) {

      console.error(err)

      setError(
        "Unable to execute the query."
      )

    } finally {

      setExecuting(false)

    }
  }



  async function routeAndExecuteQuery() {
    try {
      setRouting(true)
      setExecuting(true)
      setError("")
      setRouteResult(null)
      setExecuteResult(null)

      const query = encodeURIComponent(selectedQuery)
      const [routeResponse, executeResponse] = await Promise.all([
        fetch(`${API}/api/route?query_type=${query}`, { method: "POST" }),
        fetch(`${API}/api/execute?query_type=${query}`, { method: "POST" }),
      ])

      if (!routeResponse.ok || !executeResponse.ok) {
        throw new Error("Routing or execution failed")
      }

      const [routeData, executeData] = await Promise.all([
        routeResponse.json(),
        executeResponse.json(),
      ])
      setRouteResult(routeData)
      setExecuteResult(executeData)
    } catch (err) {
      console.error(err)
      setError("Unable to route and execute the query. Check that the backend and MongoDB are running.")
    } finally {
      setRouting(false)
      setExecuting(false)
    }
  }

  function exportResearchResults(format) {
    if (!analytics) {
      setError("Research results are not loaded yet. Please refresh the dashboard.")
      return
    }

    const exportDate = new Date().toISOString()
    const rows = queryTypeData.map((item) => ({
      query_type: item.query_type,
      query_count: item.count,
      native_avg_ms: item.native_ms,
      rule_router_avg_ms: item.router_ms,
      empirical_best_avg_ms: item.best_ms,
      router_accuracy_percent: item.accuracy,
      improvement_vs_native_percent: item.improvement,
    }))

    if (format === "json") {
      downloadTextFile(
        "dqi_research_results.json",
        JSON.stringify({ exported_at: exportDate, summary, query_types: rows, raw_analytics: analytics }, null, 2),
        "application/json;charset=utf-8"
      )
      return
    }

    if (format === "csv") {
      const headers = Object.keys(rows[0] || {
        query_type: "", query_count: "", native_avg_ms: "",
        rule_router_avg_ms: "", empirical_best_avg_ms: "",
        router_accuracy_percent: "", improvement_vs_native_percent: "",
      })
      const escapeCsv = (value) => {
        if (value === null || value === undefined) return ""
        const text = String(value)
        return /[",\n\r]/.test(text) ? `"${text.replace(/"/g, '""')}"` : text
      }
      const csv = [
        headers.join(","),
        ...rows.map((row) => headers.map((header) => escapeCsv(row[header])).join(",")),
      ].join("\r\n")
      downloadTextFile("dqi_query_type_results.csv", csv, "text/csv;charset=utf-8")
      return
    }

    const report = [
      "# Dynamic Query-Aware Index Routing for Spatio-Temporal Data in Document-Oriented NoSQL Systems",
      "",
      `Exported at: ${exportDate}`,
      "",
      "## Overall Experimental Summary",
      "",
      `- Total workload queries: ${summary.total_queries ?? "Not available"}`,
      `- Router accuracy: ${summary.router_accuracy ?? "Not available"}%`,
      `- Native MongoDB average execution time: ${summary.native_avg_ms ?? "Not available"} ms`,
      `- Rule Router average execution time: ${summary.router_avg_ms ?? "Not available"} ms`,
      `- Empirical Best average execution time: ${summary.best_avg_ms ?? "Not available"} ms`,
      `- Router improvement versus native MongoDB: ${summary.router_improvement ?? "Not available"}%`,
      "",
      "## Results by Query Type",
      "",
      "| Query type | Queries | Native (ms) | Rule Router (ms) | Empirical Best (ms) | Router accuracy (%) | Improvement (%) |",
      "|---|---:|---:|---:|---:|---:|---:|",
      ...rows.map((row) => `| ${row.query_type} | ${row.query_count ?? ""} | ${row.native_avg_ms ?? ""} | ${row.rule_router_avg_ms ?? ""} | ${row.empirical_best_avg_ms ?? ""} | ${row.router_accuracy_percent ?? ""} | ${Number(row.improvement_vs_native_percent ?? 0).toFixed(2)} |`),
      "",
      "Note: This report exports the values returned by the project's analytics API. It does not create new benchmark measurements.",
      "",
    ].join("\n")
    downloadTextFile("dqi_research_report.md", report, "text/markdown;charset=utf-8")
  }

  const summary =
    analytics?.summary || {}


  const queryTypeData =
    analytics?.query_types?.map(
      (item) => ({
        ...item,

        improvement:
          item.native_ms > 0
            ? (
                (
                  item.native_ms -
                  item.router_ms
                ) /
                item.native_ms
              ) * 100
            : 0,
      })
    ) || []


  const performanceData = [
    {
      name: "Native MongoDB",
      time: Number(
        summary.native_avg_ms || 0
      ),
    },
    {
      name: "Rule Router",
      time: Number(
        summary.router_avg_ms || 0
      ),
    },
    {
      name: "Empirical Best",
      time: Number(
        summary.best_avg_ms || 0
      ),
    },
  ]


  const routingDistribution =
    analytics?.routing?.routing_distribution?.map(
      (item) => ({
        name:
          INDEX_LABELS[item.index] ||
          INDEX_LABELS[item.selected_index] ||
          item.index ||
          item.selected_index,

        value: Number(
          item.count || 0
        ),
      })
    ) || []


  const bestDistribution =
    analytics?.routing?.best_distribution?.map(
      (item) => ({
        name:
          INDEX_LABELS[item.index] ||
          INDEX_LABELS[item.best_index] ||
          item.index ||
          item.best_index,

        value: Number(
          item.count || 0
        ),
      })
    ) || []


  return (

    <div className="app">

      <header className="app-header">

        <div className="header-content">

          <div className="header-title">

            <h1>
              Dynamic Query-Aware Index Routing
            </h1>

            <p>
              Spatio-temporal data optimization in
              document-oriented NoSQL systems
            </p>

          </div>

          <div className="system-status">

            <span
              className={`status-dot ${
                health?.status === "ok"
                  ? "online"
                  : ""
              }`}
            />

            <span>
              {health?.status === "ok"
                ? "MongoDB Connected"
                : "Connecting..."}
            </span>

          </div>

        </div>

      </header>


      <nav className="tab-navigation">

        <div className="tab-container">

          {TABS.map((tab) => (

            <button
              key={tab.id}
              className={`tab-button ${
                activeTab === tab.id
                  ? "active"
                  : ""
              }`}
              onClick={() =>
                setActiveTab(tab.id)
              }
            >
              {tab.label}
            </button>

          ))}

        </div>

      </nav>


      <main className="dashboard-container">

        {error && (
          <div className="error-banner">
            {error}
          </div>
        )}


        {/* ===================================================
            OVERVIEW
           =================================================== */}

        {activeTab === "overview" && (

          <section className="dashboard-page">

            <PageHeading
              title="Research Overview"
              subtitle="Experimental dashboard for dynamic index selection over spatio-temporal taxi data."
            />

            <div className="metric-grid">

              <MetricCard
                label="Dataset"
                value="495,160"
                subtext="MongoDB documents"
              />

              <MetricCard
                label="Workload"
                value={
                  summary.total_queries || 54
                }
                subtext="experimental queries"
              />

              <MetricCard
                label="Router Accuracy"
                value={formatPercent(
                  summary.router_accuracy
                )}
                subtext="empirical best-index match"
                highlight
              />

              <MetricCard
                label="Average Improvement"
                value={formatPercent(
                  summary.router_improvement
                )}
                subtext="vs native MongoDB"
              />

            </div>


            <div className="overview-grid">

              <div className="panel architecture-panel">

                <PanelTitle
                  title="System Architecture"
                  subtitle="Dataset → Storage → Indexing → Routing → Execution"
                />

                <div className="architecture">

                  <div className="architecture-row">

                    <ArchitectureItem
                      number="01"
                      text="NYC Taxi Dataset"
                      color="blue"
                    />

                    <Arrow />

                    <ArchitectureItem
                      number="02"
                      text="MongoDB Collection"
                      color="purple"
                    />

                    <Arrow />

                    <ArchitectureItem
                      number="03"
                      text="Candidate Indexes"
                      color="orange"
                    />

                    <Arrow />

                    <ArchitectureItem
                      number="04"
                      text="Query Workload"
                      color="green"
                    />

                  </div>

                  <div className="architecture-connector">
                    ↓
                  </div>

                  <div className="architecture-row bottom">

                    <ArchitectureItem
                      number="05"
                      text="Feature Extraction"
                      color="cyan"
                    />

                    <Arrow />

                    <ArchitectureItem
                      number="06"
                      text="Index Router"
                      color="pink"
                    />

                    <Arrow />

                    <ArchitectureItem
                      number="07"
                      text="Query Execution"
                      color="dark"
                    />

                  </div>

                </div>

              </div>


              <div className="panel finding-panel">

                <PanelTitle
                  title="Key Finding"
                />

                <div className="accuracy-highlight">

                  <span>
                    Router Accuracy
                  </span>

                  <strong>
                    {formatPercent(
                      summary.router_accuracy
                    )}
                  </strong>

                  <small>
                    Empirical best-index match
                  </small>

                </div>

                <div className="improvement-small">

                  <div>

                    <span>
                      Average execution-time reduction
                    </span>

                    <small>
                      compared with native MongoDB
                    </small>

                  </div>

                  <strong>
                    {formatPercent(
                      summary.router_improvement
                    )}
                  </strong>

                </div>

                <div className="finding-stats">

                  <MiniStat
                    label="Native MongoDB"
                    value={formatMs(
                      summary.native_avg_ms
                    )}
                  />

                  <MiniStat
                    label="Rule Router"
                    value={formatMs(
                      summary.router_avg_ms
                    )}
                  />

                  <MiniStat
                    label="Empirical Best"
                    value={formatMs(
                      summary.best_avg_ms
                    )}
                  />

                </div>

              </div>

            </div>


            <div className="panel">

              <PanelTitle
                title="Research Scope"
              />

              <div className="scope-grid">

                <ScopeItem
                  title="Temporal"
                  text="Time-range based pickup queries"
                />

                <ScopeItem
                  title="Spatial"
                  text="Geospatial radius queries"
                />

                <ScopeItem
                  title="Spatio-temporal"
                  text="Combined spatial and temporal filters"
                />

                <ScopeItem
                  title="Attributes"
                  text="Passenger count and trip distance"
                />

                <ScopeItem
                  title="Routing"
                  text="Dynamic candidate-index selection"
                />

                <ScopeItem
                  title="Benchmarking"
                  text="Native, routed and empirical-best comparison"
                />

              </div>

            </div>

          </section>

        )}


        {/* ===================================================
            LIVE ROUTER
           =================================================== */}

        {activeTab === "router" && (

          <section className="dashboard-page">

            <PageHeading
              title="Live Query Router"
              subtitle="Select a query pattern and test the routing decision directly against MongoDB."
              badge="LIVE"
            />

            <div className="router-grid">

              <div className="router-left-column">

                <div className="panel">

                  <PanelTitle
                    title="Query Configuration"
                  />

                  <label className="input-label">
                    Query Type
                  </label>

                  <select
                    className="query-select"
                    value={selectedQuery}
                    onChange={(e) => {

                      setSelectedQuery(
                        e.target.value
                      )

                      setRouteResult(null)
                      setExecuteResult(null)

                    }}
                  >

                    {QUERY_TYPES.map(
                      (type) => (

                        <option
                          key={type}
                        >
                          {type}
                        </option>

                      )
                    )}

                  </select>

                  <div className="button-row">

                    <button
                      className="primary-button"
                      onClick={routeQuery}
                      disabled={routing}
                    >
                      {routing
                        ? "Routing..."
                        : "Route Query"}
                    </button>

                    <button
                      className="secondary-button"
                      onClick={executeQuery}
                      disabled={executing}
                    >
                      {executing
                        ? "Executing..."
                        : "Execute Query"}
                    </button>
                    <button
                      className="tertiary-button"
                      onClick={routeAndExecuteQuery}
                      disabled={routing || executing}
                    >
                      {routing || executing
                        ? "Testing..."
                        : "Route + Execute"}
                    </button>

                  </div>

                  <div className="query-description">

                    <strong>
                      {selectedQuery}
                    </strong>

                    <p>
                      {getQueryDescription(
                        selectedQuery
                      )}
                    </p>

                  </div>

                </div>


                <div className="panel routing-logic-panel">

                  <PanelTitle
                    title="Routing Logic"
                  />

                  <div className="logic-grid">

                    <LogicRule
                      condition="Spatial + Temporal"
                      result="Compound Index"
                    />

                    <LogicRule
                      condition="Spatial only"
                      result="Spatial Index"
                    />

                    <LogicRule
                      condition="Temporal only"
                      result="Temporal Index"
                    />

                    <LogicRule
                      condition="Spatial + Attribute"
                      result="Spatial Index"
                    />

                    <LogicRule
                      condition="Temporal + Attribute"
                      result="Temporal Index"
                    />

                  </div>

                </div>

              </div>


              <div className="router-right-column">

                <div className="panel">

                  <PanelTitle
                    title="Query Features"
                  />

                  <div className="feature-grid">

                    <Feature
                      label="Spatial Query"
                      value={getFeature(
                        selectedQuery,
                        "spatial"
                      )}
                    />

                    <Feature
                      label="Temporal Query"
                      value={getFeature(
                        selectedQuery,
                        "temporal"
                      )}
                    />

                    <Feature
                      label="Attribute Query"
                      value={getFeature(
                        selectedQuery,
                        "attribute"
                      )}
                    />

                  </div>

                  {routeResult && (

                    <div className="recommendation">

                      <span>
                        Recommended Index
                      </span>

                      <strong>
                        {routeResult.recommended_index ||
                          "—"}
                      </strong>

                    </div>

                  )}

                </div>


                {executeResult && (

                  <div className="panel execution-panel">

                    <div className="panel-title-row">

                      <PanelTitle
                        title="Live MongoDB Execution"
                      />

                      <span className="success-label">
                        Executed
                      </span>

                    </div>

                    <div className="execution-grid">

                      <LiveMetric
                        label="Execution Time"
                        value={formatMs(
                          executeResult.execution_time_ms
                        )}
                      />

                      <LiveMetric
                        label="Documents Returned"
                        value={formatNumber(
                          executeResult.documents_returned
                        )}
                      />

                      <LiveMetric
                        label="Documents Examined"
                        value={formatNumber(
                          executeResult.documents_examined
                        )}
                      />

                      <LiveMetric
                        label="Keys Examined"
                        value={formatNumber(
                          executeResult.keys_examined
                        )}
                      />

                      <LiveMetric
                        label="Selected Index"
                        value={
                          executeResult.recommended_index ||
                          "—"
                        }
                      />

                      <LiveMetric
                        label="Query Type"
                        value={
                          executeResult.query_type ||
                          selectedQuery
                        }
                      />

                    </div>

                  </div>

                )}

              </div>

            </div>

          </section>

        )}


        {/* ===================================================
            PERFORMANCE
           =================================================== */}

        {activeTab === "performance" && (

          <section className="dashboard-page">

            <PageHeading
              title="Performance Dashboard"
              subtitle="Average execution-time comparison across the complete workload."
            />

            <div className="metric-grid three">

              <MetricCard
                label="Native MongoDB"
                value={formatMs(
                  summary.native_avg_ms
                )}
                subtext="average execution time"
              />

              <MetricCard
                label="Rule Router"
                value={formatMs(
                  summary.router_avg_ms
                )}
                subtext="average execution time"
                highlight
              />

              <MetricCard
                label="Empirical Best"
                value={formatMs(
                  summary.best_avg_ms
                )}
                subtext="best candidate per query"
              />

            </div>

            <div className="performance-layout">

              <div className="performance-left">

                <div className="panel performance-chart-panel">

                  <PanelTitle
                    title="Average Execution Time"
                    subtitle="Lower is better"
                  />

                  <div className="chart-large">

                    <ResponsiveContainer
                      width="100%"
                      height="100%"
                    >

                      <BarChart
                        data={performanceData}
                      >

                        <CartesianGrid
                          strokeDasharray="3 3"
                        />

                        <XAxis
                          dataKey="name"
                        />

                        <YAxis />

                        <Tooltip />

                        <Legend />

                        <Bar
                          dataKey="time"
                          name="Execution Time (ms)"
                          fill="#2563eb"
                          barSize={55}
                          radius={[
                            5,
                            5,
                            0,
                            0,
                          ]}
                        />

                      </BarChart>

                    </ResponsiveContainer>

                  </div>

                </div>


                <div className="panel interpretation-panel">

                  <PanelTitle
                    title="Interpretation"
                  />

                  <div className="interpretation">

                    <p>
                      <b>Native MongoDB:</b>{" "}
                      execution using the database's
                      normal optimizer behavior.
                    </p>

                    <p>
                      <b>Rule Router:</b>{" "}
                      selects a candidate index based
                      on extracted query characteristics.
                    </p>

                    <p>
                      <b>Empirical Best:</b>{" "}
                      fastest candidate index measured
                      for each query.
                    </p>

                    <div className="note">
                      The empirical-best result is an
                      experimental reference for evaluating
                      routing accuracy.
                    </div>

                  </div>

                </div>

              </div>


              <div className="performance-right">

                <div className="panel performance-summary-panel">

                  <PanelTitle
                    title="Performance Summary"
                  />

                  <Comparison
                    label="Router vs Native MongoDB"
                    value={formatPercent(
                      summary.router_improvement
                    )}
                  />

                  <Comparison
                    label="Empirical Best vs Native"
                    value={formatPercent(
                      summary.best_improvement
                    )}
                  />

                  <Comparison
                    label="Router Gap from Empirical Best"
                    value={formatPercent(
                      Math.abs(
                        summary.router_gap_from_best ||
                        0
                      )
                    )}
                    neutral
                  />

                  <Comparison
                    label="Documents Examined Reduction"
                    value={formatPercent(
                      summary.docs_examined_reduction
                    )}
                  />

                  <Comparison
                    label="Keys Examined Reduction"
                    value={formatPercent(
                      summary.keys_reduction_percent ||
                      summary.keys_examined_reduction
                    )}
                  />

                </div>

              </div>

            </div>

            <div className="panel research-export-panel">
              <div className="export-copy">
                <PanelTitle
                  title="Research Results Export"
                  subtitle="Download the currently loaded experimental summary and query-type results."
                />
                <p className="note-text">
                  Exports use the analytics already loaded by this dashboard; they do not rerun benchmarks or invent measurements.
                </p>
              </div>
              <div className="export-actions">
                <button className="export-button" onClick={() => exportResearchResults("markdown")} disabled={!analytics}>
                  Download Report (.md)
                </button>
                <button className="export-button" onClick={() => exportResearchResults("csv")} disabled={!analytics}>
                  Download Results (.csv)
                </button>
                <button className="export-button" onClick={() => exportResearchResults("json")} disabled={!analytics}>
                  Download Data (.json)
                </button>
              </div>
            </div>

          </section>

        )}


        {/* ===================================================
            ROUTING ANALYSIS
           =================================================== */}

        {activeTab === "routing" && (

          <section className="dashboard-page">

            <PageHeading
              title="Routing Analysis"
              subtitle="Analyze how accurately the router selects the empirically fastest candidate index."
            />

            <div className="metric-grid three">

              <MetricCard
                label="Router Accuracy"
                value={formatPercent(
                  summary.router_accuracy
                )}
                subtext="empirical best-index match"
                highlight
              />

              <MetricCard
                label="Correct Decisions"
                value={
                  analytics?.routing?.correct ??
                  51
                }
                subtext="out of 54 queries"
              />

              <MetricCard
                label="Candidate Indexes"
                value={
                  summary.candidate_indexes || 3
                }
                subtext="tested per query"
              />

            </div>


            <div className="routing-analysis-layout">

              <div className="routing-pie-column">

                <div className="panel routing-pie-panel">

                  <PanelTitle
                    title="Router Selection Distribution"
                  />

                  {routingDistribution.length > 0 ? (

                    <div className="chart-pie routing-pie-small">

                      <ResponsiveContainer
                        width="100%"
                        height="100%"
                      >

                        <PieChart>

                          <Pie
                            data={routingDistribution}
                            dataKey="value"
                            nameKey="name"
                            cx="34%"
                            cy="50%"
                            outerRadius={56}
                            labelLine={false}
                            label={({
                              cx,
                              cy,
                              midAngle,
                              innerRadius,
                              outerRadius,
                              value,
                            }) => {

                              const RADIAN =
                                Math.PI / 180

                              const radius =
                                innerRadius +
                                (
                                  outerRadius -
                                  innerRadius
                                ) * 0.55

                              const x =
                                cx +
                                radius *
                                Math.cos(
                                  -midAngle *
                                  RADIAN
                                )

                              const y =
                                cy +
                                radius *
                                Math.sin(
                                  -midAngle *
                                  RADIAN
                                )

                              return (
                                <text
                                  x={x}
                                  y={y}
                                  fill="#ffffff"
                                  textAnchor="middle"
                                  dominantBaseline="central"
                                  fontSize={12}
                                  fontWeight={800}
                                >
                                  {value}
                                </text>
                              )
                            }}
                          >

                            {routingDistribution.map(
                              (_, index) => (

                                <Cell
                                  key={`router-cell-${index}`}
                                  fill={
                                    PIE_COLORS[
                                      index %
                                      PIE_COLORS.length
                                    ]
                                  }
                                />

                              )
                            )}

                          </Pie>

                          <Tooltip />

                          <Legend
                            layout="vertical"
                            align="right"
                            verticalAlign="middle"
                            wrapperStyle={{
                              fontSize: "11px",
                              lineHeight: "22px",
                            }}
                          />

                        </PieChart>

                      </ResponsiveContainer>

                    </div>

                  ) : (

                    <div className="empty routing-pie-empty">
                      Routing distribution unavailable.
                    </div>

                  )}

                </div>


                <div className="panel routing-pie-panel">

                  <PanelTitle
                    title="Empirical Best Distribution"
                  />

                  {bestDistribution.length > 0 ? (

                    <div className="chart-pie routing-pie-small">

                      <ResponsiveContainer
                        width="100%"
                        height="100%"
                      >

                        <PieChart>

                          <Pie
                            data={bestDistribution}
                            dataKey="value"
                            nameKey="name"
                            cx="34%"
                            cy="50%"
                            outerRadius={56}
                            labelLine={false}
                            label={({
                              cx,
                              cy,
                              midAngle,
                              innerRadius,
                              outerRadius,
                              value,
                            }) => {

                              const RADIAN =
                                Math.PI / 180

                              const radius =
                                innerRadius +
                                (
                                  outerRadius -
                                  innerRadius
                                ) * 0.55

                              const x =
                                cx +
                                radius *
                                Math.cos(
                                  -midAngle *
                                  RADIAN
                                )

                              const y =
                                cy +
                                radius *
                                Math.sin(
                                  -midAngle *
                                  RADIAN
                                )

                              return (
                                <text
                                  x={x}
                                  y={y}
                                  fill="#ffffff"
                                  textAnchor="middle"
                                  dominantBaseline="central"
                                  fontSize={12}
                                  fontWeight={800}
                                >
                                  {value}
                                </text>
                              )
                            }}
                          >

                            {bestDistribution.map(
                              (_, index) => (

                                <Cell
                                  key={`best-cell-${index}`}
                                  fill={
                                    PIE_COLORS[
                                      index %
                                      PIE_COLORS.length
                                    ]
                                  }
                                />

                              )
                            )}

                          </Pie>

                          <Tooltip />

                          <Legend
                            layout="vertical"
                            align="right"
                            verticalAlign="middle"
                            wrapperStyle={{
                              fontSize: "11px",
                              lineHeight: "22px",
                            }}
                          />

                        </PieChart>

                      </ResponsiveContainer>

                    </div>

                  ) : (

                    <div className="empty routing-pie-empty">
                      Best-index distribution unavailable.
                    </div>

                  )}

                </div>

              </div>


              <div className="panel routing-accuracy-panel">

                <PanelTitle
                  title="Routing Accuracy by Query Type"
                />

                <div className="accuracy-grid">

                  {queryTypeData.map(
                    (item) => (

                      <div
                        className="accuracy-card"
                        key={item.query_type}
                      >

                        <span>
                          {item.query_type}
                        </span>

                        <strong>
                          {formatPercent(
                            item.accuracy
                          )}
                        </strong>

                        <div className="progress">

                          <div
                            className="progress-bar"
                            style={{
                              width: `${item.accuracy}%`,
                            }}
                          />

                        </div>

                      </div>

                    )
                  )}

                </div>

              </div>

            </div>

          </section>

        )}


        {/* ===================================================
            QUERY ANALYSIS
           =================================================== */}

        {activeTab === "query" && (

          <section className="dashboard-page">

            <PageHeading
              title="Query-Type Analysis"
              subtitle="Performance and routing behavior across the six workload categories."
            />


            <div className="query-analysis-panels">


              <div className="panel workload-performance-panel">

                <PanelTitle
                  title="Workload Performance"
                  subtitle="Average execution time"
                />

                <div className="table-container">

                  <table>

                    <thead>

                      <tr>

                        <th>
                          Query Type
                        </th>

                        <th>
                          Queries
                        </th>

                        <th>
                          Native
                        </th>

                        <th>
                          Rule Router
                        </th>

                        <th>
                          Empirical Best
                        </th>

                        <th>
                          Accuracy
                        </th>

                        <th>
                          Improvement
                        </th>

                      </tr>

                    </thead>


                    <tbody>

                      {queryTypeData.map(
                        (item) => (

                          <tr
                            key={item.query_type}
                          >

                            <td className="query-name">
                              {item.query_type}
                            </td>

                            <td>
                              {item.count}
                            </td>

                            <td>
                              {formatMs(
                                item.native_ms
                              )}
                            </td>

                            <td className="router-text">
                              {formatMs(
                                item.router_ms
                              )}
                            </td>

                            <td>
                              {formatMs(
                                item.best_ms
                              )}
                            </td>

                            <td>

                              <span
                                className={`accuracy ${
                                  Number(
                                    item.accuracy
                                  ) >= 90
                                    ? "good"
                                    : "warning"
                                }`}
                              >

                                {formatPercent(
                                  item.accuracy
                                )}

                              </span>

                            </td>

                            <td className="improvement">

                              {formatPercent(
                                item.improvement
                              )}

                            </td>

                          </tr>

                        )
                      )}

                    </tbody>

                  </table>

                </div>

              </div>


              {/* =================================================
                  ONLY THIS CHART SECTION HAS BEEN MODIFIED
                 ================================================= */}

              <div className="panel query-improvement-panel">

                <PanelTitle
                  title="Improvement by Query Type"
                />

                <div
                  className="chart-medium"
                  style={{
                    width: "100%",
                    position: "relative",
                  }}
                >

                  <div
                    style={{
                      width: "88%",
                      height: "165px",
                      margin: "0 auto",
                    }}
                  >

                    <ResponsiveContainer
                      width="100%"
                      height="100%"
                    >

                      <BarChart
                        data={queryTypeData}
                        margin={{
                          top: 5,
                          right: 5,
                          left: 0,
                          bottom: 5,
                        }}
                        barCategoryGap="25%"
                      >

                        <CartesianGrid
                          strokeDasharray="3 3"
                        />

                        <XAxis
                          dataKey="query_type"
                          tick={false}
                          axisLine={true}
                          tickLine={false}
                        />

                        <YAxis
                          domain={[0, 40]}
                          tick={{
                            fontSize: 10,
                          }}
                        />

                        <Tooltip />

                        <Bar
                          dataKey="improvement"
                          name="Execution-time reduction (%)"
                          barSize={30}
                          radius={[
                            5,
                            5,
                            0,
                            0,
                          ]}
                        >

                          {queryTypeData.map(
                            (item, index) => (

                              <Cell
                                key={`query-chart-cell-${index}`}
                                fill={
                                  QUERY_CHART_COLORS[
                                    index %
                                    QUERY_CHART_COLORS.length
                                  ]
                                }
                              />

                            )
                          )}

                        </Bar>

                      </BarChart>

                    </ResponsiveContainer>

                  </div>


                  {/* Query-type labels moved below the chart */}

                  <div
                    style={{
                      width: "96%",
                      margin: "4px auto 0",
                      display: "flex",
                      justifyContent: "center",
                      alignItems: "flex-start",
                      flexWrap: "wrap",
                      gap: "7px 14px",
                    }}
                  >

                    {queryTypeData.map(
                      (item, index) => (

                        <div
                          key={`query-label-${index}`}
                          style={{
                            display: "flex",
                            alignItems: "center",
                            gap: "5px",
                            fontSize: "10px",
                            fontWeight: 600,
                            color: "#334155",
                            whiteSpace: "nowrap",
                          }}
                        >

                          <span
                            style={{
                              width: "8px",
                              height: "8px",
                              borderRadius: "2px",
                              backgroundColor:
                                QUERY_CHART_COLORS[
                                  index %
                                  QUERY_CHART_COLORS.length
                                ],
                              display: "inline-block",
                              flexShrink: 0,
                            }}
                          />

                          <span>
                            {item.query_type}
                          </span>

                        </div>

                      )
                    )}

                  </div>

                </div>

              </div>

            </div>

          </section>

        )}


        {/* ===================================================
            INDEXES
           =================================================== */}

        {activeTab === "indexes" && (

          <section className="dashboard-page">

            <PageHeading
              title="Candidate Indexes"
              subtitle="Index structures evaluated by the routing experiment."
            />

            <div className="index-grid">

              <IndexCard
                number="01"
                type="T"
                title="Temporal Index"
                code="pickup_time_1"
                description="Optimizes queries that primarily filter documents using pickup time."
                use="Temporal queries"
              />

              <IndexCard
                number="02"
                type="S"
                title="Spatial Index"
                code="pickup_location_2dsphere"
                description="Optimizes geospatial queries using the pickup location."
                use="Spatial queries"
              />

              <IndexCard
                number="03"
                type="ST"
                title="Compound Index"
                code="pickup_location_2dsphere_pickup_time_1"
                description="Combines geospatial and temporal filtering for spatio-temporal queries."
                use="Spatio-temporal queries"
              />

            </div>


            <div className="panel">

              <PanelTitle
                title="Index Routing Rules"
              />

              <div className="routing-table">

                <div className="routing-header">

                  <span>
                    Spatial
                  </span>

                  <span>
                    Temporal
                  </span>

                  <span>
                    Attribute
                  </span>

                  <span>
                    Selected Index
                  </span>

                </div>

                <RoutingRow
                  spatial="Yes"
                  temporal="Yes"
                  attribute="Any"
                  index="pickup_location_2dsphere_pickup_time_1"
                />

                <RoutingRow
                  spatial="Yes"
                  temporal="No"
                  attribute="Any"
                  index="pickup_location_2dsphere"
                />

                <RoutingRow
                  spatial="No"
                  temporal="Yes"
                  attribute="Any"
                  index="pickup_time_1"
                />

                <RoutingRow
                  spatial="No"
                  temporal="No"
                  attribute="Any"
                  index="NO_INDEX"
                />

              </div>

            </div>


            <div className="panel">

              <PanelTitle
                title="Experimental Note"
              />

              <p className="note-text">
                The experiment evaluates three candidate
                indexes. The router extracts query
                characteristics and selects an appropriate
                candidate before query execution.
              </p>

            </div>

          </section>

        )}

      </main>
    </div>
  )
}


/* =========================================================
   COMPONENTS
   ========================================================= */

function PageHeading({
  title,
  subtitle,
  badge,
}) {

  return (

    <div className="page-heading">

      <div>

        <h2>
          {title}
        </h2>

        <p>
          {subtitle}
        </p>

      </div>

      {badge && (

        <span className="badge">
          {badge}
        </span>

      )}

    </div>

  )
}


function PanelTitle({
  title,
  subtitle,
}) {

  return (

    <div className="panel-title">

      <h3>
        {title}
      </h3>

      {subtitle && (

        <span>
          {subtitle}
        </span>

      )}

    </div>

  )
}


function MetricCard({
  label,
  value,
  subtext,
  highlight = false,
}) {

  return (

    <div
      className={`metric-card ${
        highlight
          ? "highlight"
          : ""
      }`}
    >

      <span>
        {label}
      </span>

      <strong>
        {value}
      </strong>

      <small>
        {subtext}
      </small>

    </div>

  )
}


function MiniStat({
  label,
  value,
}) {

  return (

    <div className="mini-stat">

      <span>
        {label}
      </span>

      <strong>
        {value}
      </strong>

    </div>

  )
}


function ArchitectureItem({
  number,
  text,
  color,
}) {

  return (

    <div
      className={`architecture-item ${color}`}
    >

      <span>
        {number}
      </span>

      <strong>
        {text}
      </strong>

    </div>

  )

}


function Arrow() {

  return (
    <div className="architecture-arrow">
      →
    </div>
  )

}


function ScopeItem({
  title,
  text,
}) {

  return (

    <div className="scope-item">

      <strong>
        {title}
      </strong>

      <span>
        {text}
      </span>

    </div>

  )

}


function Feature({
  label,
  value,
}) {

  return (

    <div className="feature">

      <span>
        {label}
      </span>

      <strong>
        {value ? "YES" : "NO"}
      </strong>

    </div>

  )

}


function LiveMetric({
  label,
  value,
}) {

  return (

    <div className="live-metric">

      <span>
        {label}
      </span>

      <strong>
        {value}
      </strong>

    </div>

  )

}


function LogicRule({
  condition,
  result,
}) {

  return (

    <div className="logic-rule">

      <span>
        {condition}
      </span>

      <b>
        →
      </b>

      <strong>
        {result}
      </strong>

    </div>

  )

}


function Comparison({
  label,
  value,
  neutral = false,
}) {

  return (

    <div className="comparison">

      <span>
        {label}
      </span>

      <strong
        className={
          neutral
            ? "neutral"
            : ""
        }
      >
        {value}
      </strong>

    </div>

  )

}


function IndexCard({
  number,
  type,
  title,
  code,
  description,
  use,
}) {

  return (

    <div className="index-card">

      <div className="index-top">

        <div className="index-icon">
          {type}
        </div>

        <span className="index-number">
          {number}
        </span>

      </div>

      <h3>
        {title}
      </h3>

      <code>
        {code}
      </code>

      <p>
        {description}
      </p>

      <div className="index-use">

        <span>
          Primary use
        </span>

        <strong>
          {use}
        </strong>

      </div>

    </div>

  )

}


function RoutingRow({
  spatial,
  temporal,
  attribute,
  index,
}) {

  return (

    <div className="routing-row">

      <span>
        {spatial}
      </span>

      <span>
        {temporal}
      </span>

      <span>
        {attribute}
      </span>

      <code>
        {index}
      </code>

    </div>

  )

}


/* =========================================================
   HELPERS
   ========================================================= */

function getFeature(
  queryType,
  feature
) {

  const spatial = [
    "Spatial",
    "Spatio-temporal",
    "Spatial + Attribute",
    "Spatio-temporal + Attribute",
  ].includes(queryType)


  const temporal = [
    "Temporal",
    "Spatio-temporal",
    "Temporal + Attribute",
    "Spatio-temporal + Attribute",
  ].includes(queryType)


  const attribute = [
    "Temporal + Attribute",
    "Spatial + Attribute",
    "Spatio-temporal + Attribute",
  ].includes(queryType)


  if (feature === "spatial") {
    return spatial
  }

  if (feature === "temporal") {
    return temporal
  }

  if (feature === "attribute") {
    return attribute
  }

  return false
}


function getQueryDescription(
  queryType
) {

  const descriptions = {

    Temporal:
      "Filters taxi trips using a pickup-time range.",

    Spatial:
      "Filters taxi trips within a geographic radius around a pickup location.",

    "Spatio-temporal":
      "Combines geographic and pickup-time constraints.",

    "Temporal + Attribute":
      "Combines pickup-time filtering with an attribute condition.",

    "Spatial + Attribute":
      "Combines geographic filtering with an attribute condition.",

    "Spatio-temporal + Attribute":
      "Combines spatial, temporal and attribute constraints.",

  }


  return descriptions[queryType] || ""
}


export default App