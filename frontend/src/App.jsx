import { useEffect, useState } from "react";

function getSeverityColor(level) {
  switch(level){
    case "high":
      return "red";
    case "medium":
      return "orange";
    case "low":
      return "green";
    default:
      return "gray";
  }
}

function App() {
  const [metrics,setMetrics]=useState(null);
  const [incidents,setIncidents]=useState([]);

  useEffect(()=>{

    fetch("http://127.0.0.1:8000/metrics")
      .then(res=>res.json())
      .then(data=>setMetrics(data));

    fetch("http://127.0.0.1:8000/incidents")
      .then(res=>res.json())
      .then(data=>setIncidents(data.incidents));

  },[]);

  return (
    <div style={{padding:"30px",fontFamily:"Arial"}}>

      <h1>🚨 InfraMind AI Dashboard</h1>

      {metrics && (
        <div
          style={{
            display:"flex",
            gap:"20px",
            marginBottom:"30px"
          }}
        >

          <div style={{
            border:"1px solid gray",
            padding:"15px"
          }}>
            <h3>Total</h3>
            <h2>{metrics.total_incidents}</h2>
          </div>

          <div style={{
            border:"1px solid gray",
            padding:"15px"
          }}>
            <h3>Open</h3>
            <h2>{metrics.status_counts.open}</h2>
          </div>

          <div style={{
            border:"1px solid gray",
            padding:"15px"
          }}>
            <h3>Investigating</h3>
            <h2>{metrics.status_counts.investigating}</h2>
          </div>

        </div>
      )}

      <h2>Incident List</h2>

      <table
        border="1"
        cellPadding="10"
        style={{
          borderCollapse:"collapse",
          width:"100%"
        }}
      >

        <thead>
          <tr>
            <th>ID</th>
            <th>Log</th>
            <th>Type</th>
            <th>Severity</th>
            <th>Status</th>
          </tr>
        </thead>

        <tbody>

          {incidents.map((incident)=>(

            <tr key={incident.id}>
              <td>{incident.id}</td>

              <td>{incident.log_text}</td>

              <td>{incident.incident_type}</td>

              <td>

                <span
                  style={{
                    color:"white",
                    background:getSeverityColor(
                      incident.severity
                    ),
                    padding:"5px 10px",
                    borderRadius:"10px"
                  }}
                >
                  {incident.severity}
                </span>

              </td>

              <td>{incident.status}</td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>
  );
}

export default App;