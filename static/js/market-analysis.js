document.addEventListener('DOMContentLoaded', function() {
    const marketForm = document.getElementById('marketAnalysisForm');
    const analysisResults = document.getElementById('analysisResults');

    marketForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const userIdea = document.getElementById('businessIdea').value;
        analysisResults.innerHTML = "<p>Fetching live market insights...</p>";

        fetch('/analyze-market', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ idea: userIdea })
        })
        .then(response => response.json())
        .then(data => {
            analysisResults.innerHTML = formatMarketAnalysis(data.analysis);
            requestAnimationFrame(() => {
                renderChart();
            });
        })
        .catch(error => {
            analysisResults.innerHTML = "<p style='color:red;'>Error fetching market data.</p>";
            console.error(error);
        });
    });

    function formatMarketAnalysis(responseText) {
        let formattedHTML = `<h3>Market Analysis</h3>`;

        // Splitting the response into sections
        let sections = responseText.split('###');

        sections.forEach(section => {
            if (section.includes('Competitors in')) {
                formattedHTML += `<h4>Competitors</h4><ul>`;
                section.match(/\*\*(.*?)\*\*/g)?.forEach(company => {
                    formattedHTML += `<li><strong>${company.replace(/\*\*/g, '')}</strong></li>`;
                });
                formattedHTML += `</ul>`;
            } 
            else if (section.includes('Potential Investors')) {
                formattedHTML += `<h4>Investors</h4><ul>`;
                section.match(/\*\*(.*?)\*\*/g)?.forEach(investor => {
                    formattedHTML += `<li><strong>${investor.replace(/\*\*/g, '')}</strong></li>`;
                });
                formattedHTML += `</ul>`;
            }
            else {
                formattedHTML += `<p>${section}</p>`;
            }
        });

        return formattedHTML;
    }
    let marketChart = null; // Store the chart instance globally

    function renderChart() {
        let ctx = document.getElementById("marketShareChart").getContext("2d");
    
        // Destroy previous chart instance if it exists
        if (marketChart) {
            marketChart.destroy();
        }
    
        // Create new chart instance
        marketChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ["Tech", "Healthcare", "Finance", "E-commerce", "Others"],
                datasets: [{
                    data: [35, 25, 15, 15, 10], // Static Data
                    backgroundColor: ["#912ae6", "#b763d1", "#e1f5fe", "#ffcc80", "#80deea"]
                }]
            }
        });
    }
});


