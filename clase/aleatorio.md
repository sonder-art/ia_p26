---
title: "Aleatorio"
permalink: /aleatorio/
---

<div class="max-w-4xl mx-auto">

<div class="text-center mb-12">
  <div class="inline-block text-accent text-lg font-bold mb-8 px-4 py-3 rounded-lg bg-bg-secondary/50">
    GENERADOR ALEATORIO
  </div>

  <div class="mt-6">
    <img src="{{ '/images/kaiji_random_number_generator.png' | url }}" alt="Kaiji Random Number Generator" class="mx-auto w-full max-w-2xl rounded-xl shadow-2xl border-2 border-accent/30">
  </div>
</div>

<div class="random-generator mt-8 p-8 rounded-2xl bg-gradient-to-br from-accent/5 to-accent-secondary/5 border-2 border-accent/20">

  <!-- Range Inputs -->
  <div class="grid grid-cols-2 gap-6 mb-8">
    <div class="space-y-2">
      <label for="min-range" class="block text-sm font-medium text-text-muted">Mínimo</label>
      <input
        type="number"
        id="min-range"
        value="1"
        class="w-full px-4 py-3 rounded-lg bg-bg-secondary border-2 border-border focus:border-accent text-text text-xl font-mono transition-all"
      />
    </div>
    <div class="space-y-2">
      <label for="max-range" class="block text-sm font-medium text-text-muted">Máximo</label>
      <input
        type="number"
        id="max-range"
        value="100"
        class="w-full px-4 py-3 rounded-lg bg-bg-secondary border-2 border-border focus:border-accent text-text text-xl font-mono transition-all"
      />
    </div>
  </div>

  <!-- Generate Button -->
  <button id="generate-btn" class="w-full py-4 px-6 rounded-xl bg-accent hover:bg-accent/90 text-bg font-bold text-lg transition-all transform hover:scale-105 active:scale-95 shadow-lg hover:shadow-accent/50">
    [&gt;] Generar Número
  </button>

  <!-- Result Display -->
  <div id="result-container" class="mt-8 hidden">
    <div class="relative overflow-hidden">
      <div class="text-center py-12 px-6 rounded-2xl bg-gradient-to-br from-bg-secondary to-bg-tertiary border-2 border-accent/50 shadow-2xl">
        <div class="text-sm text-text-muted mb-2 uppercase tracking-wider">Resultado</div>
        <div id="result-number" class="text-7xl font-bold text-accent font-mono result-animate" style="text-shadow: 0 0 20px currentColor;">
          0
        </div>
        <div id="result-range" class="text-sm text-text-muted mt-4">
          Rango: 1 - 100
        </div>
      </div>
      <!-- Particle effects -->
      <div class="particles-container absolute inset-0 pointer-events-none"></div>
    </div>
  </div>

  <!-- History -->
  <div id="history-container" class="mt-6 hidden">
    <div class="text-sm text-text-muted mb-3 flex items-center gap-2">
      <span>Historial</span>
      <button id="clear-history" class="ml-auto text-xs px-2 py-1 rounded bg-bg-tertiary hover:bg-accent/20 transition-colors">
        Limpiar
      </button>
    </div>
    <div id="history-list" class="flex flex-wrap gap-2"></div>
  </div>

</div>

<style>
@keyframes slideIn {
  from {
    transform: translateY(-20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes pulse-glow {
  0%, 100% {
    box-shadow: 0 0 20px rgba(0, 255, 65, 0.3);
  }
  50% {
    box-shadow: 0 0 40px rgba(0, 255, 65, 0.6);
  }
}

@keyframes number-roll {
  0% {
    transform: rotateX(0deg);
    opacity: 0;
  }
  50% {
    transform: rotateX(180deg);
    opacity: 0.5;
  }
  100% {
    transform: rotateX(360deg);
    opacity: 1;
  }
}

@keyframes particle-float {
  0% {
    transform: translateY(0) translateX(0) scale(0);
    opacity: 1;
  }
  100% {
    transform: translateY(-100px) translateX(var(--tx)) scale(1);
    opacity: 0;
  }
}

.result-animate {
  animation: number-roll 0.5s ease-out;
}

.particle {
  position: absolute;
  width: 8px;
  height: 8px;
  background: var(--color-accent);
  border-radius: 50%;
  animation: particle-float 1s ease-out forwards;
  bottom: 50%;
  left: 50%;
}

#result-container.show {
  animation: slideIn 0.5s ease-out;
}

#generate-btn:active {
  animation: pulse-glow 0.3s ease-out;
}
</style>

<script>
(function() {
  const minInput = document.getElementById('min-range');
  const maxInput = document.getElementById('max-range');
  const generateBtn = document.getElementById('generate-btn');
  const resultContainer = document.getElementById('result-container');
  const resultNumber = document.getElementById('result-number');
  const resultRange = document.getElementById('result-range');
  const historyContainer = document.getElementById('history-container');
  const historyList = document.getElementById('history-list');
  const clearHistoryBtn = document.getElementById('clear-history');
  const particlesContainer = document.querySelector('.particles-container');

  let history = [];

  function createParticles() {
    particlesContainer.innerHTML = '';
    for (let i = 0; i < 15; i++) {
      const particle = document.createElement('div');
      particle.className = 'particle';
      particle.style.setProperty('--tx', `${(Math.random() - 0.5) * 200}px`);
      particle.style.animationDelay = `${Math.random() * 0.2}s`;
      particlesContainer.appendChild(particle);
    }
  }

  function generateRandom() {
    const min = parseInt(minInput.value);
    const max = parseInt(maxInput.value);

    if (isNaN(min) || isNaN(max)) {
      alert('Por favor ingresa números válidos');
      return;
    }

    if (min >= max) {
      alert('El mínimo debe ser menor que el máximo');
      return;
    }

    // Animate button
    generateBtn.style.transform = 'scale(0.95)';
    setTimeout(() => {
      generateBtn.style.transform = '';
    }, 100);

    // Generate random number
    const random = Math.floor(Math.random() * (max - min + 1)) + min;

    // Show result with animation
    resultContainer.classList.remove('hidden');
    resultContainer.classList.add('show');

    // Animate number change
    resultNumber.style.animation = 'none';
    setTimeout(() => {
      resultNumber.style.animation = 'number-roll 0.5s ease-out';
      resultNumber.textContent = random;
    }, 10);

    resultRange.textContent = `Rango: ${min} - ${max}`;

    // Create particle effect
    createParticles();

    // Add to history
    history.unshift({ number: random, min, max, time: new Date() });
    if (history.length > 10) history.pop();
    updateHistory();
  }

  function updateHistory() {
    if (history.length === 0) {
      historyContainer.classList.add('hidden');
      return;
    }

    historyContainer.classList.remove('hidden');
    historyList.innerHTML = history.map((item, idx) => `
      <div class="px-3 py-2 rounded-lg bg-bg-secondary border border-border text-sm font-mono ${idx === 0 ? 'ring-2 ring-accent/50' : ''}" style="animation: slideIn 0.3s ease-out">
        <span class="text-accent font-bold">${item.number}</span>
        <span class="text-text-muted text-xs ml-2">(${item.min}-${item.max})</span>
      </div>
    `).join('');
  }

  function clearHistory() {
    history = [];
    updateHistory();
  }

  generateBtn.addEventListener('click', generateRandom);
  clearHistoryBtn.addEventListener('click', clearHistory);

  // Allow Enter key to generate
  minInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') generateRandom();
  });
  maxInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') generateRandom();
  });
})();
</script>

</div>
