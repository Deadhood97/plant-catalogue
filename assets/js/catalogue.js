const API_URL = 'https://plant-catalogue.onrender.com';

// --- Rendering Logic ---

function renderGrid(filteredPlants, container) {
    if (!container) return;
    container.innerHTML = "";
    if (filteredPlants.length === 0) {
        container.innerHTML = `
          <div class="col-span-full py-20 text-center text-leaf/60">
              <p class="text-2xl font-serif mb-2">🌿</p>
              <p class="text-lg">No plants found matching these filters.</p>
          </div>`;
        return;
    }

    const fragment = document.createDocumentFragment();

    filteredPlants.forEach((plant, index) => {
        const card = document.createElement('div');
        // Staggered list animation
        card.style.animationDelay = `${index * 50}ms`;
        card.className = "card-hover group bg-white rounded-3xl overflow-hidden shadow-sm border border-stone-100 flex flex-col relative h-96 cursor-pointer";

        // Make entire card clickable
        card.onclick = () => openModal(plant);

        // --- Image Section (Tall) ---
        const imgContainer = document.createElement('div');
        imgContainer.className = "relative h-2/3 overflow-hidden bg-stone-100";

        const img = document.createElement('img');
        // Handle both local photos/thumbnails and public absolute URLs
        let thumbPath = plant.reference_image.url;

        // HOTFIX: If DB has "localhost" URL but we are in Prod, rewrite it
        if (thumbPath.includes('localhost') && API_URL.startsWith('https')) {
            const parts = thumbPath.split('/uploads/');
            if (parts.length > 1) thumbPath = `${API_URL}/uploads/${parts[1]}`;
        }

        if (!thumbPath.startsWith('http')) {
            thumbPath = thumbPath.replace("photos/", "thumbnails/");
        }
        img.src = thumbPath;
        img.className = "w-full h-full object-cover transition-transform duration-700 group-hover:scale-110";
        img.loading = "lazy";

        // Badge: Personality
        if (plant.plant_personality) {
            const vibe = document.createElement('div');
            vibe.className = "absolute top-3 right-3 bg-white/90 backdrop-blur text-jungle text-xs font-bold px-3 py-1.5 rounded-full shadow-lg z-10";
            vibe.textContent = plant.plant_personality;
            imgContainer.appendChild(vibe);
        }

        // Badge: Confidence Ring
        if (plant.confidence) {
            const confPercent = Math.round(plant.confidence * 100);
            const ring = document.createElement('div');
            let color = confPercent >= 90 ? "border-emerald-500 text-emerald-600" : "border-amber-500 text-amber-600";
            ring.className = `absolute top-3 left-3 w-10 h-10 rounded-full bg-white flex items-center justify-center text-[10px] font-bold border-2 ${color} shadow-lg`;
            ring.textContent = `${confPercent}%`;
            imgContainer.appendChild(ring);
        }

        imgContainer.appendChild(img);
        card.appendChild(imgContainer);

        // --- Simple Body ---
        const body = document.createElement('div');
        body.className = "p-5 flex flex-col justify-between h-1/3";

        // Title
        const titleBox = document.createElement('div');
        titleBox.innerHTML = `<h2 class="font-serif text-xl font-bold text-jungle leading-tight truncate">${plant.identified_name}</h2>
                          <p class="text-leaf/60 text-sm italic truncate">${plant.scientific_name}</p>`;
        body.appendChild(titleBox);

        // Footer Icons
        const iconDiv = document.createElement('div');
        iconDiv.className = "flex gap-1";
        if (plant.is_flowering) iconDiv.innerHTML += '<span title="Flowering" class="bg-pink-50 text-pink-600 p-1 rounded">🌸</span>';
        if (plant.is_edible) iconDiv.innerHTML += '<span title="Edible" class="bg-amber-50 text-amber-600 p-1 rounded">🥗</span>';
        if (plant.is_medicinal) iconDiv.innerHTML += '<span title="Medicinal" class="bg-blue-50 text-blue-600 p-1 rounded">💊</span>';
        if (plant.is_toxic_to_pets) iconDiv.innerHTML += '<span title="Toxic" class="bg-red-50 text-red-600 p-1 rounded">⚠️</span>';

        const footer = document.createElement('div');
        footer.className = "flex items-center justify-between mt-auto";
        footer.appendChild(iconDiv);

        const viewBtn = document.createElement('span');
        viewBtn.className = "text-terracotta text-sm font-medium flex items-center gap-1 group-hover:gap-2 transition-all";
        viewBtn.innerHTML = 'View <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" /></svg>';
        footer.appendChild(viewBtn);

        body.appendChild(footer);
        card.appendChild(body);
        fragment.appendChild(card);
    });

    container.appendChild(fragment);
}

// --- Modal Logic ---

function openModal(plant) {
    const m = document.getElementById('detailModal');
    const img = document.getElementById('modalImg');

    // 1. Header Data
    let thumbPath = plant.reference_image.url;

    // HOTFIX: If DB has "localhost" URL but we are in Prod, rewrite it
    if (thumbPath.includes('localhost') && API_URL.startsWith('https')) {
        const parts = thumbPath.split('/uploads/');
        if (parts.length > 1) thumbPath = `${API_URL}/uploads/${parts[1]}`;
    }

    if (!thumbPath.startsWith('http')) {
        thumbPath = thumbPath.replace("photos/", "thumbnails/");
    }
    img.src = thumbPath;
    document.getElementById('modalName').textContent = plant.identified_name;
    document.getElementById('modalSci').textContent = plant.scientific_name;

    // 2. Badges
    const badgeContainer = document.getElementById('modalBadges');
    badgeContainer.innerHTML = '';
    if (plant.plant_personality)
        addBadge(badgeContainer, `🎭 ${plant.plant_personality}`, "bg-terracotta text-white");

    if (plant.is_flowering) addBadge(badgeContainer, "🌸 Flowering", "bg-pink-100 text-pink-700");
    if (plant.is_edible) addBadge(badgeContainer, "🥗 Edible", "bg-amber-100 text-amber-700");
    if (plant.is_medicinal) addBadge(badgeContainer, "💊 Medicinal", "bg-blue-100 text-blue-700");
    if (plant.is_toxic_to_pets) addBadge(badgeContainer, "⚠️ Toxic to Pets", "bg-red-100 text-red-700");

    // 3. Bio
    const localNames = (plant.local_names || []).map(l => l.name).join(', ') || "None known";
    document.getElementById('modalLocal').textContent = localNames;

    const life = plant.lifespan ? ` • ${plant.lifespan}` : '';
    document.getElementById('modalOrigin').textContent = (plant.origin_region || "Unknown") + life;

    const fact = plant.fun_fact?.text || "No specific fun fact available.";
    document.getElementById('modalFactBox').innerHTML = `<span class="font-bold">Did you know?</span> "${fact}"`;

    // 4. Care Grid
    const careContainer = document.getElementById('modalCareGrid');
    careContainer.innerHTML = '';
    const care = plant.care || {};

    const careItems = [
        { l: "Water", v: care.watering_frequency, i: "💧" },
        { l: "Sun", v: care.sunlight_requirement, i: "☀️" },
        { l: "Soil", v: care.soil_type, i: "🪴" },
        { l: "Growth", v: care.growth_rate, i: "📈" }
    ];

    careItems.forEach(item => {
        const div = document.createElement('div');
        div.className = "bg-stone-50 rounded-lg p-3 border border-stone-100";
        div.innerHTML = `<p class="text-[10px] uppercase text-leaf/50 font-bold tracking-wider mb-1">${item.i} ${item.l}</p>
                        <p class="text-sm font-medium text-jungle leading-snug">${item.v || 'Unknown'}</p>`;
        careContainer.appendChild(div);
    });

    // 5. Symbolism
    const symBox = document.getElementById('modalSymbolism');
    if (plant.symbolism) {
        symBox.style.display = "block";
        symBox.innerHTML = `<h4 class="font-serif text-lg text-purple-900 mb-2">✨ Symbolism</h4><p class="text-purple-800/80 italic">${plant.symbolism}</p>`;
    } else {
        symBox.style.display = "none";
    }

    // Show Modal
    m.showModal();
    document.body.style.overflow = 'hidden';
}

function closeModal() {
    const m = document.getElementById('detailModal');
    m.close();
    document.body.style.overflow = '';
}

function addBadge(parent, text, classes) {
    const span = document.createElement('span');
    span.className = `px-3 py-1 rounded-full text-xs font-bold ${classes}`;
    span.textContent = text;
    parent.appendChild(span);
}

// --- Filtering & Sorting ---

function filterAndSortPlants(plants, inputs) {
    const { searchInput, attrCheckboxes, confFilter, sortSelect } = inputs;
    let result = [...plants];

    // 1. Search (Name or Local Name)
    const query = searchInput.value.toLowerCase();
    if (query) {
        result = result.filter(p =>
            p.identified_name.toLowerCase().includes(query) ||
            (p.local_names && p.local_names.some(l => l.name.toLowerCase().includes(query)))
        );
    }

    // 2. Attributes (AND logic: must match all checked)
    attrCheckboxes.forEach(cb => {
        if (cb.checked) {
            const key = cb.value;
            result = result.filter(p => p[key] === true);
        }
    });

    // 3. Confidence
    const minConf = parseFloat(confFilter.value);
    if (minConf > 0) {
        result = result.filter(p => (p.confidence || 0) >= minConf);
    }

    // 4. Sort
    const sortMode = sortSelect.value;
    result.sort((a, b) => {
        switch (sortMode) {
            case 'name_asc':
                return a.identified_name.localeCompare(b.identified_name);
            case 'name_desc':
                return b.identified_name.localeCompare(a.identified_name);
            case 'conf_desc':
                return (b.confidence || 0) - (a.confidence || 0);
            case 'conf_asc':
                return (a.confidence || 0) - (b.confidence || 0);
            case 'date_desc':
                return new Date(b.date_added || 0) - new Date(a.date_added || 0);
            case 'date_asc':
                return new Date(a.date_added || 0) - new Date(b.date_added || 0);
            default:
                return 0;
        }
    });

    return result;
}

// Global initialization of modal listeners (to avoid repeating it in every page)
document.addEventListener('DOMContentLoaded', () => {
    const closeBtn = document.getElementById('modalCloseBtn');
    if (closeBtn) closeBtn.addEventListener('click', closeModal);

    const modal = document.getElementById('detailModal');
    if (modal) {
        modal.addEventListener('click', (e) => {
            const rect = e.target.getBoundingClientRect();
            if (rect.left > e.clientX || rect.right < e.clientX || rect.top > e.clientY || rect.bottom < e.clientY) {
                closeModal();
            }
        });
        modal.addEventListener('close', () => {
            document.body.style.overflow = '';
        });
    }
});
