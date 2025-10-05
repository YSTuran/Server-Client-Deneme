async function sendMessage() {
  const message = document.getElementById('message').value;
  const method = document.getElementById('method').value;
  const key = document.getElementById('key').value;
  const mode = document.getElementById('mode').value;

  const resp = await fetch('/send', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({message, method, key, mode})
  });

  const data = await resp.json();
  if (resp.ok) {
    document.getElementById('cipherOut').textContent = data.cipher;
    document.getElementById('decodedOut').textContent = data.decoded;
  } else {
    document.getElementById('cipherOut').textContent = 'Hata: ' + (data.error || JSON.stringify(data));
    document.getElementById('decodedOut').textContent = '';
  }
}

async function loadInbox() {
  const resp = await fetch('/inbox');
  const d = await resp.json();
  document.getElementById('inbox').textContent = JSON.stringify(d.messages, null, 2);
}

document.getElementById('sendBtn').addEventListener('click', sendMessage);
document.getElementById('refresh').addEventListener('click', loadInbox);

loadInbox();
