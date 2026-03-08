let editIndex = null;

    function escapeHtml(unsafe) {
      return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
    }

    // load password from backend
    async function loadPasswords() {
      const res = await fetch('/api/passwords');
      const data = await res.json();
      const tbody = document.getElementById('table-body');
      tbody.innerHTML = '';

      // get all data then show the table in html
      data.forEach(item => {
        const tr = document.createElement('tr');
        if (item.strong) tr.classList.add('strong');
        if (!item.strong && item.password) tr.classList.add('weak');
        if (item.repeated) tr.classList.add('repeat');

        tr.innerHTML = `
              <td class="font-medium text-gray-900">${escapeHtml(item.site)}</td>
              <td class="copy-cell">
                ${item.site ? `
                  <button class="action-btn" onclick="copyToClipboard('${escapeHtml(item.site)}')" title="Copy site">
                    <i class="fa-regular fa-copy"></i>
                  </button>
                ` : '—'}
              </td>
              <td class="font-medium text-gray-900">${escapeHtml(item.username)}</td>
              <td class="copy-cell">
                ${item.username ? `
                  <button class="action-btn" onclick="copyToClipboard('${escapeHtml(item.username)}')" title="Copy username">
                    <i class="fa-regular fa-copy"></i>
                  </button>
                ` : '—'}
              </td>
              <td class="font-mono text-gray-700 tracking-wide">
                ${item.password ? '••••••••' : '—'}
              </td>
              <td class="copy-cell">
                ${item.password ? `
                  <button class="action-btn" onclick="copyToClipboard('${escapeHtml(item.password)}')" title="Copy password">
                    <i class="fa-regular fa-copy"></i>
                  </button>
                ` : ''}
              </td>
              <td class="${item.expired ? 'text-red-500 font-medium' : 'text-gray-700'}">
                ${item.expired 
                  ? (item.expiry || '—')
                  : (item.expiry || '—')}
              </td>
              <td class="text-center">
                ${item.file 
                  ? `<a href="/files/${escapeHtml(item.file)}" download class="text-blue-600 hover:underline text-sm font-medium">${escapeHtml(item.file)}</a>`
                  : '<span class="text-gray-400">—</span>'}
              </td>
              <td class="text-center text-xl">
                ${item.strong 
                  ? '<i class="fa-solid fa-check-circle text-emerald-600" title="Strong password"></i>' 
                  : '<i class="fa-solid fa-circle-xmark text-red-500" title="Weak password"></i>'}
              </td>
              <td class="text-center text-xl">
                ${item.repeated 
                  ? '<i class="fa-solid fa-exclamation-circle text-amber-600" title="Password is repeated"></i>' 
                  : '<span class="text-gray-300">—</span>'}
              </td>
              <td class="whitespace-nowrap text-right space-x-2">
                <button class="action-btn" onclick="editEntry(${item.index})">Edit</button>
                <button class="action-btn delete-btn" onclick="deleteEntry(${item.index})">Delete</button>
              </td>
            `;
        tbody.appendChild(tr);
      });
    }

    // add copy function
    function copyToClipboard(text) {
      navigator.clipboard.writeText(text)
      .catch(() => {
        alert('Failed to copy');
      });
    }

    // send from data to backend and generate a new password
    async function generatePassword() {
      const maxLen = document.getElementById('max_length').value;
      const special = document.getElementById('special').checked;
      const numbersOnly = document.getElementById('numbers-only').checked;
      const firstLetter = document.getElementById('first-letter').checked;

      const res = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          max_length: maxLen, 
          require_special: special, 
          numbers_only: numbersOnly, 
          first_letter: firstLetter 
        })
      });

      const data = await res.json();
      if (data.password) {
        document.getElementById('password').value = data.password;
      } else {
        alert(data.error || 'Password generation failed');
      }
    }

    // find the data show it on fields
    function editEntry(index) {
      fetch('/api/passwords')
        .then(r => r.json())
        .then(data => {
          const entry = data.find(e => e.index === index);
          if (!entry) return;

          document.getElementById('edit-index').value = index;
          document.getElementById('site').value = entry.site;
          document.getElementById('username').value = entry.username;
          document.getElementById('password').value = entry.password || '';
          document.getElementById('expiry').value = entry.expiry;
          document.getElementById('file-name').textContent = entry.file || 'No file selected';

          document.getElementById('form-title').textContent = 'Edit Entry';
          document.getElementById('save-btn').textContent = 'UPDATE';
          document.getElementById('cancel-edit').style.display = 'inline-block';
          editIndex = index;
        });
    }

    // just call api to delete 
    async function deleteEntry(index) {
      if (!confirm('Delete this entry?')) return;
      await fetch(`/api/password/${index}`, { method: 'DELETE' });
      loadPasswords();
    }

    //clean the fields
    function resetForm() {
      document.getElementById('password-form').reset();
      document.getElementById('edit-index').value = '';
      document.getElementById('file-name').textContent = 'No file selected';
      document.getElementById('form-title').textContent = 'Password Form';
      document.getElementById('save-btn').textContent = 'SAVE';
      document.getElementById('cancel-edit').style.display = 'none';
      editIndex = null;
      document.getElementById('expiry').value = new Date(Date.now() + 90*24*60*60*1000).toISOString().split('T')[0];
    }

    // Event listeners
    document.getElementById('generate-btn').onclick = generatePassword;

    document.getElementById('attach-btn').onclick = () => document.getElementById('file').click();

    document.getElementById('file').onchange = e => {
      const f = e.target.files[0];
      if (f) document.getElementById('file-name').textContent = f.name;
    };

    document.getElementById('clear-file-btn').onclick = () => {
      document.getElementById('file').value = '';
      document.getElementById('file-name').textContent = 'No file selected';
    };

    document.getElementById('cancel-edit').onclick = resetForm;

    document.getElementById('password-form').onsubmit = async e => {
      e.preventDefault();
      const formData = new FormData(e.target);

      // call api to update or save
      try {
        const res = await fetch('/api/password', {
          method: 'POST',
          body: formData
        });
        const result = await res.json();
        if (res.ok) {
          alert(editIndex !== null ? 'Entry updated!' : 'Entry saved!');
          resetForm();
          loadPasswords();
        } else {
          alert(result.error || 'An error occurred');
        }
      } catch (err) {
        alert('Network error – please try again');
      }
    };

    // Initialize
    document.addEventListener('DOMContentLoaded', () => {
      document.getElementById('expiry').value = new Date(Date.now() + 90*24*60*60*1000).toISOString().split('T')[0];
      loadPasswords();
    });