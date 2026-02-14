document.addEventListener("DOMContentLoaded", () => {
    const API_BASE = "http://127.0.0.1:5000";

    // 1. Fetch Total Trips
    fetch(`${API_BASE}/total-trips`)
      .then(res => res.json())
      .then(data => {
        const el = document.getElementById("totalTrips");
        if (el) el.innerText = Number(data.total_trips).toLocaleString();
      })
      .catch(err => console.error("KPI Fetch Error:", err));

    // 2. Fetch Borough Chart
    fetch(`${API_BASE}/trips-by-borough`)
      .then(res => res.json())
      .then(data => {
        console.log("Chart Data Received:", data);

        // CLEANING: Handle 'NaN' or nulls found in your dataset
        const cleanedData = data.filter(item => 
            item.borough && 
            item.borough !== "NaN" && 
            item.borough !== "Unknown"
        );

        const labels = cleanedData.map(item => item.borough);
        const counts = cleanedData.map(item => item.trip_count);

        const canvas = document.getElementById("boroughChart");
        if (!canvas) {
            console.error("Canvas element 'boroughChart' not found in HTML");
            return;
        }
        
        const ctx = canvas.getContext("2d");

        // Destroy existing instance to prevent "Canvas already in use" error
        if (window.myChartInstance instanceof Chart) {
            window.myChartInstance.destroy();
        }

        // Initialize Chart
        window.myChartInstance = new Chart(ctx, {
          type: "bar",
          data: {
            labels: labels,
            datasets: [{
              label: "Trips",
              data: counts,
              backgroundColor: [
                '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'
              ],
              borderRadius: 6
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
              y: { 
                beginAtZero: true,
                ticks: {
                    // Format large numbers (e.g., 6M) for better UX
                    callback: (value) => value.toLocaleString()
                }
              }
            }
          }
        });
      })
      .catch(err => {
          console.error("Chart Fetch Error:", err);
          // Only update if the element exists to avoid crashing
          const chartStatus = document.getElementById("boroughChart");
          if (chartStatus) {
              chartStatus.parentElement.innerHTML = `<p style="text-align:center; padding:20px;">Error: ${err.message}</p>`;
          }
      });
});