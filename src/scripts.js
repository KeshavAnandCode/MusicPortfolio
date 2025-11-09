// Fetch and render music library
fetch('data/music_metadata.json')
  .then(response => response.json())
  .then(data => {
    const library = document.getElementById('music-library');

    // Separate featured and normal tracks
    const featuredTracks = data.filter(track => track.featured).slice(0, 3); // limit to 3
    let normalTracks = data.filter(track => !track.featured);

    // === Featured Tracks ===
    if (featuredTracks.length > 0) {

      const featuredHeading = document.createElement('h2');
      featuredHeading.textContent = 'Featured';
      featuredHeading.style.marginBottom = '1rem';
      library.appendChild(featuredHeading);



      const featuredContainer = document.createElement('div');
      featuredContainer.className = 'featured-container';
      featuredContainer.style.display = 'flex';
      featuredContainer.style.gap = '1rem';
      featuredContainer.style.marginBottom = '2rem';
      featuredContainer.style.justifyContent = 'space-between';

      featuredTracks.forEach(track => {
        const div = document.createElement('div');
        div.className = 'track featured-track';
        div.style.flex = '1';           // equal width
        div.style.minWidth = '250px';   // reasonable minimum width
        div.style.padding = '1rem';
        div.style.display = 'flex';
        div.style.flexDirection = 'column';
        div.style.justifyContent = 'space-between';
        div.style.borderRadius = '8px';
        div.style.boxShadow = '0 2px 4px rgba(0,0,0,0.1)';

        // Title (Movie)
        const title = document.createElement('h3');
        title.textContent = track.movie
          ? `${track.title} (${track.movie})`
          : track.title;
        div.appendChild(title);

        // Genre | Desc | Date
        const metaParts = [track.genre];
        if (track.desc) metaParts.push(track.desc);
        if (track.date) metaParts.push(track.date);
        const meta = document.createElement('p');
        meta.textContent = metaParts.filter(Boolean).join(' | ');
        div.appendChild(meta);

        // Audio player
        const audio = document.createElement('audio');
        audio.controls = true;
        audio.src = track.path_mp3 || track.path_flac;
        div.appendChild(audio);

        featuredContainer.appendChild(div);
      });

      library.appendChild(featuredContainer);
    }

    // === Sorting Dropdown ===
    const sortContainer = document.createElement('div');
    sortContainer.style.marginBottom = '1rem';
    sortContainer.innerHTML = `
      <label for="sort-select">Sort by: </label>
      <select id="sort-select">
        <option value="recent">Most Recent</option>
        <option value="oldest">Oldest</option>
      </select>
    `;
    library.appendChild(sortContainer);

    const allTracksContainer = document.createElement('div');
    allTracksContainer.id = 'all-tracks';
    library.appendChild(allTracksContainer);

    function renderTracks(tracksArray) {
      allTracksContainer.innerHTML = ''; // clear previous
      tracksArray.forEach(track => {
        const div = document.createElement('div');
        div.className = 'track';

        const title = document.createElement('h3');
        title.textContent = track.movie
          ? `${track.title} (${track.movie})`
          : track.title;
        div.appendChild(title);

        const metaParts = [track.genre];
        if (track.desc) metaParts.push(track.desc);
        if (track.date) metaParts.push(track.date);
        const meta = document.createElement('p');
        meta.textContent = metaParts.filter(Boolean).join(' | ');
        div.appendChild(meta);

        const audio = document.createElement('audio');
        audio.controls = true;
        audio.src = track.path_mp3 || track.path_flac;
        div.appendChild(audio);

        allTracksContainer.appendChild(div);
      });
    }

    // Initial render (most recent)
    normalTracks.sort((a, b) => new Date(b.date) - new Date(a.date));
    renderTracks(normalTracks);

    // Handle dropdown change
    document.getElementById('sort-select').addEventListener('change', e => {
      if (e.target.value === 'recent') {
        normalTracks.sort((a, b) => new Date(b.date) - new Date(a.date));
      } else if (e.target.value === 'oldest') {
        normalTracks.sort((a, b) => new Date(a.date) - new Date(b.date));
      }
      renderTracks(normalTracks);
    });
  })
  .catch(err => console.error('Error loading music JSON:', err));