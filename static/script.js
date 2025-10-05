document.getElementById('sendBtn').addEventListener('click', async () => {
  const message = document.getElementById('message').value;
  const method = document.getElementById('method').value;
  const key = document.getElementById('key').value;

  const resp = await fetch('/send', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({message, method, key})
  });

  const data = await resp.json();
  if (resp.ok) {
    document.getElementById('result').textContent = data.cipher;
  } else {
    document.getElementById('result').textContent = 'Hata: ' + (data.error || JSON.stringify(data));
  }
});

document.getElementById('refresh').addEventListener('click', async () => {
  const r = await fetch('/inbox');
  const d = await r.json();
  document.getElementById('inbox').textContent = JSON.stringify(d.messages, null, 2);
});
