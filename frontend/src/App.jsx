import { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  PieChart,
  Pie,
  Cell
} from "recharts";

function getSeverityColor(level) {
  switch (level) {
    case "critical":
      return "#8B0000";
    case "high":
      return "#FF0000";
    case "medium":
      return "#FFA500";
    case "low":
      return "#008000";
    default:
      return "#808080";
  }
}

function App() {
  const [metrics, setMetrics] = useState(null);
  const [incidents, setIncidents] = useState([]);
  const [searchText, setSearchText] = useState("");
  const [severityFilter, setSeverityFilter] = useState("all");
  const [statusFilter, setStatusFilter] = useState("all");

  const loadDashboardData = () => {
    fetch("http://127.0.0.1:8000/metrics")
      .then((res) => res.json())
      .then((data) => setMetrics(data));

    fetch("http://127.0.0.1:8000/incidents")
      .then((res) => res.json())
      .then((data) => setIncidents(data.incidents || []));
  };

  useEffect(() => {
    loadDashboardData();
  }, []);

  const resolveIncident = (incidentId) => {
    fetch(
      `http://127.0.0.1:8000/incidents/${incidentId}/status?status=resolved`,
      {
        method: "PUT"
      }
    )
      .then((res) => res.json())
      .then(() => loadDashboardData());
  };

  const filteredIncidents = incidents.filter((incident) => {
    const matchesSearch =
      incident.log_text.toLowerCase().includes(searchText.toLowerCase()) ||
      incident.incident_type.toLowerCase().includes(searchText.toLowerCase());

    const matchesSeverity =
      severityFilter === "all" || incident.severity === severityFilter;

    const matchesStatus =
      statusFilter === "all" || incident.status === statusFilter;

    return matchesSearch && matchesSeverity && matchesStatus;
  });

  const severityChartData = metrics
    ? [
        { name: "High", value: metrics.severity_counts.high },
        { name: "Medium", value: metrics.severity_counts.medium },
        { name: "Low", value: metrics.severity_counts.low }
      ]
    : [];

  const statusChartData = metrics
    ? [
        { name: "Open", value: metrics.status_counts.open },
        { name: "Investigating", value: metrics.status_counts.investigating },
        { name: "Resolved", value: metrics.status_counts.resolved }
      ]
    : [];

  const colors = ["#ff0000", "#ffa500", "#008000"];

  return (
    <div style={{ padding: "30px", fontFamily: "Arial" }}>
      <h1>🚨 InfraMind AI Dashboard</h1>

      {metrics && (
        <div style={{ display: "flex", gap: "20px", marginBottom: "30px" }}>
          <div style={{ border: "1px solid gray", padding: "15px" }}>
            <h3>Total</h3>
            <h2>{metrics.total_incidents}</h2>
          </div>

          <div style={{ border: "1px solid gray", padding: "15px" }}>
            <h3>Open</h3>
            <h2>{metrics.status_counts.open}</h2>
          </div>

          <div style={{ border: "1px solid gray", padding: "15px" }}>
            <h3>Investigating</h3>
            <h2>{metrics.status_counts.investigating}</h2>
          </div>

          <div style={{ border: "1px solid gray", padding: "15px" }}>
            <h3>Resolved</h3>
            <h2>{metrics.status_counts.resolved}</h2>
          </div>
        </div>
      )}

      <h2>Charts</h2>

      <div style={{ display: "flex", gap: "60px", marginBottom: "40px" }}>
        <div>
          <h3>Severity Distribution</h3>

          <BarChart width={350} height={250} data={severityChartData}>
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="value" fill="#ff4444" />
          </BarChart>
        </div>

        <div>
          <h3>Status Distribution</h3>

          <PieChart width={350} height={250}>
            <Pie data={statusChartData} dataKey="value" outerRadius={80}>
              {statusChartData.map((entry, index) => (
                <Cell key={index} fill={colors[index]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </div>
      </div>

      <h2>Incident List</h2>

      <div style={{ display: "flex", gap: "15px", marginBottom: "20px" }}>
        <input
          type="text"
          placeholder="Search incidents..."
          value={searchText}
          onChange={(event) => setSearchText(event.target.value)}
        />

        <select
          value={severityFilter}
          onChange={(event) => setSeverityFilter(event.target.value)}
        >
          <option value="all">All Severities</option>
          <option value="critical">Critical</option>
          <option value="high">High</option>
          <option value="medium">Medium</option>
          <option value="low">Low</option>
        </select>

        <select
          value={statusFilter}
          onChange={(event) => setStatusFilter(event.target.value)}
        >
          <option value="all">All Statuses</option>
          <option value="open">Open</option>
          <option value="investigating">Investigating</option>
          <option value="resolved">Resolved</option>
        </select>
      </div>

      <p>
        Showing {filteredIncidents.length} of {incidents.length} incidents
      </p>

      <table
        border="1"
        cellPadding="10"
        style={{ width: "100%", borderCollapse: "collapse" }}
      >
        <thead>
          <tr>
            <th>ID</th>
            <th>Log</th>
            <th>Type</th>
            <th>Severity</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>

        <tbody>
          {filteredIncidents.map((incident) => (
            <tr key={incident.id}>
              <td>{incident.id}</td>
              <td>{incident.log_text}</td>
              <td>{incident.incident_type}</td>
              <td>
                <span
                  style={{
                    color: "white",
                    background: getSeverityColor(incident.severity),
                    padding: "5px 10px",
                    borderRadius: "10px"
                  }}
                >
                  {incident.severity}
                </span>
              </td>
              <td>{incident.status}</td>
              <td>
                {incident.status !== "resolved" ? (
                  <button onClick={() => resolveIncident(incident.id)}>
                    Resolve
                  </button>
                ) : (
                  "Resolved"
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;