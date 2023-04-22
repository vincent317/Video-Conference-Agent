const form = document.getElementById('form');
const resultDiv = document.getElementById('result');

async function handleSubmit(event) {
event.preventDefault();

// Remove previously generated content
resultDiv.innerHTML = '';

const meeting_id = document.getElementById('meeting_id').value;
if (!meeting_id) {
alert('Please input meeting ID.');
return;
}

const agenda_items = document.getElementById('agenda_items').value;

try {
const response = await fetch(`http://127.0.0.1:5000/meeting_info/${meeting_id}?agenda_items=${agenda_items}`, {
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
const meetingInfoSection = document.createElement('div');
meetingInfoSection.innerHTML = `
  <h2>Meeting Information:</h2><hr><br>
  <p>Meeting Title: ${data.meeting_title}</p>
  <p>Meeting Date: ${data.meeting_date}</p>
  <h3>Participants:</h3>
  <ul>
    ${Object.entries(data.participants).map(([participant, details]) => `
      <li>
        <span${details.late === 'late' ? ' style="color: red;"' : ''}>${participant} (${details.late})</span>
        <p>Speaking Time: ${details.duration}</p>
      </li>
    `).join('')}
  </ul>
`;
resultDiv.appendChild(meetingInfoSection);

// Create the summary section
const summarySection = document.createElement('div');
summarySection.innerHTML = `
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
`;
resultDiv.appendChild(summarySection);

// Create the action items section
const actionItemsSection = document.createElement('div');
actionItemsSection.innerHTML = `
  <h2>Action Items:</h2><hr><br>
  <ul>
    ${data.action_items.map(item => `<li>${item}</li>`).join('')}
  </ul>
`;
resultDiv.appendChild(actionItemsSection);

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