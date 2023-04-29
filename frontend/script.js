const form = document.getElementById('form');
const resultDiv = document.getElementById('result');

async function handleSubmit(event) {
  event.preventDefault();

  const loadingMessage = document.createElement('div');
  loadingMessage.id = 'loading-message';
  loadingMessage.innerText = 'Loading meeting report...';
  resultDiv.appendChild(loadingMessage);
  

  const meeting_id = document.getElementById('meeting_id').value;
  if (!meeting_id) {
    alert('Please input meeting ID.');
    return;
  }

  const agenda_items = document.getElementById('agenda_items').value;
  const meeting_date = document.getElementById('meeting_date').value;
  const meeting_time = document.getElementById('meeting_time').value;
  const timezoneSelector = document.getElementById('timezone');
  const timezone = encodeURIComponent(timezoneSelector.value);

  try {
    // Send request to server
    let url = encodeURI(`http://127.0.0.1:5000/meeting_info/${meeting_id}?agenda_items=${agenda_items}&timezone=${timezone}&meeting_date=${meeting_date}&meeting_time=${meeting_time}`);
    console.log(url)
    const response = await fetch(
      url,
      {
        method: 'POST',
        headers: {
          'accept': 'application/json'
        }
      });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();


    // Create the meeting info section
    const meetingInfoSection = `
  <div>
    <h2>Meeting Information:</h2><hr><br>
    <p>Meeting Title: ${data.meeting_title}</p>
    <p>Meeting Date: ${data.meeting_date} ${data.meeting_time}</p>
    <h3>Participants:</h3>
    <ul>
      ${Object.entries(data.participants).map(([participant, details]) => `
        <li>
          <span${details.late === 'late' ? ' style="color: red;"' : ''}>${participant} (${details.late})</span>
          <p>Speaking Time: ${details.duration}</p>
        </li>
      `).join('')}
    </ul>
  </div>
`;
    // Create the summary section
    const summarySection = `
  <div>
    <h2>Summary and Agenda:</h2><hr><br>
    <h3>Overall summary:</h3>
    <p>${data.summary['Overall summary']}</p>
    <h3>Short agenda summaries:</h3>
    <ul>
      ${Object.entries(data.summary['Short agenda summaries']).map(([agenda, summary]) => `
        <li>
          <h4>${agenda}</h4>
          <p>${summary}</p>
          <button onclick="toggleLongSummary('${agenda}')">Show/hide long summary</button>
          <div id="${agenda}_long_summary" style="display: none;">
            <p>${data.summary['Detailed agenda summaries'][agenda]}</p>
          </div>
        </li>
      `).join('')}
    </ul>
    <h3>Additional summaries:</h3>
    <p>${data.summary['Additional summaries']}</p>
  </div>
`;

    // Create the action items section
    const actionItemsSection = `
  <div>
    <h2>Action Items:</h2><hr><br>
    <ul>
      ${data.action_items.map(item => `<li>${item}</li>`).join('')}
    </ul>
  </div>
`;
  
  resultDiv.innerHTML = `
    ${meetingInfoSection}
    ${summarySection}
    ${actionItemsSection}
  `;

    // Create the download button
    const downloadButton = document.createElement('button');
    downloadButton.innerText = 'Download Generated Report';
    resultDiv.appendChild(downloadButton);
    downloadButton.onclick = function() {
      // Remove download button from the DOM
      downloadButton.remove();
    
      // Get the report HTML
      const reportHTML = resultDiv.innerHTML;
    
      // Create the report blob and download the file
      const reportBlob = new Blob([`
        <html>
          <head>
            <title>Meeting Report</title>
            <script src="./functions.js"></script>
          </head>
          <body>
            ${reportHTML}
          </body>
        </html>
      `], {type: 'text/html'});
      const reportURL = URL.createObjectURL(reportBlob);
      const downloadLink = document.createElement('a');
      downloadLink.href = reportURL;
      downloadLink.download = 'meeting_report.html';
      downloadLink.click();
    };
    

    loadingMessage.remove()
  

  } catch (error) {
    const errorSection = document.createElement('div');
    errorSection.innerHTML = `
  <h2>Error:</h2><hr><br>
  <p>${error.message}</p>
`;
    resultDiv.appendChild(errorSection);
  }
}


function toggleLongSummary(agenda) {
  const longSummary = document.getElementById(`${agenda}_long_summary`);
  longSummary.style.display = longSummary.style.display === 'none' ? 'block' : 'none';
}
