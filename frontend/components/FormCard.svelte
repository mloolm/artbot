<script>
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();

  // Импортируем данные о странах
  import countryData from '../data/countries.json'; 
  
  // Подготовка данных: теперь только для гражданства (4-й столбец)
  const countries = Object.entries(countryData).map(([code, names]) => ({
    code: code,
    englishName: names[0],  
    russianName: names[1],  
    valueCitizenship: names[3], 
    
  }));

  // Карта для быстрого поиска названий по коду
  const countryMap = new Map(countries.map(c => [c.code, c]));
  
  // --- ЭКСПОРТИРУЕМЫЕ ПЕРЕМЕННЫЕ ---
  export let firstName = '';
  export let lastName = '';
  export let email = ''; 
  
  // Код гражданства
  export let citizenshipCode = ''; 
  
  // --- ЛОКАЛЬНЫЕ ПЕРЕМЕННЫЕ ---
  let citizenshipInput = ''; 
  

  // --- ЛОГИКА АВТОПОДСТАНОВКИ ---

  // Унифицированная функция фильтрации
  function filterCountries(input) {
      if (!input) return [];
      const searchLower = input.toLowerCase();
      return countries.filter(country =>
          country.russianName.toLowerCase().includes(searchLower) || 
          country.englishName.toLowerCase().includes(searchLower)   
      );
  }

  // Вычисляемый список стран для Гражданства 
  $: filteredCitizenshipCountries = filterCountries(citizenshipInput);
  
  // Проверка выбора страны 
  $: isCitizenshipSelected = citizenshipCode && countryMap.get(citizenshipCode)?.russianName === citizenshipInput;


  // --- ЛОГИКА РЕЖИМА РЕДАКТИРОВАНИЯ (СИНХРОНИЗАЦИЯ КОДОВ ВВОДА) ---

  // Синхронизация для гражданства
  $: if (citizenshipCode && !citizenshipInput) {
      const country = countryMap.get(citizenshipCode);
      if (country) citizenshipInput = country.russianName;
  }
  
  // --- ОБРАБОТЧИКИ ВЫБОРА ---

  function selectCitizenship(country) {
    citizenshipInput = country.russianName; 
    citizenshipCode = country.code; // Устанавливаем код
  }
  
  // --- ОБРАБОТЧИК ОТПРАВКИ ФОРМЫ ---
  function handleSubmit() {
    // Находим финальное значение для отправки
    const citizenshipValue = countryMap.get(citizenshipCode)?.valueCitizenship;

    
    // Отправляем событие 'submit' с обновленным набором данных
    dispatch('submit', { 
      firstName, 
      lastName, 
      email, 
      citizenshipCode,
      citizenshipValue,
    });
  }
</script>

<form on:submit|preventDefault={handleSubmit} class="space-y-4">

  <div class="space-y-1">
    <label for="firstName" class="block font-medium text-gray-700">Имя (как в загранпаспорте)</label>
    <input
      id="firstName"
      type="text"
      placeholder="Введите имя"
      bind:value={firstName}
      required
      class="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-[#0088cc] focus:border-[#0088cc]"
    />
  </div>

  <div class="space-y-1">
    <label for="lastName" class="block font-medium text-gray-700">Фамилия (как в загранпаспорте)</label>
    <input
      id="lastName"
      type="text"
      placeholder="Введите фамилию"
      bind:value={lastName}
      required
      class="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-[#0088cc] focus:border-[#0088cc]"
    />
  </div>

  <div class="space-y-1">
    <label for="email" class="block font-medium text-gray-700">Email</label>
    <input
      id="email"
      type="email"
      placeholder="email@example.com"
      bind:value={email}
      required
      class="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-[#0088cc] focus:border-[#0088cc]"
    />
  </div>

  <div class="space-y-1 relative">
    <label for="citizenship" class="block font-medium text-gray-700">Гражданство</label>
    <input
      id="citizenship"
      type="text"
      placeholder="Начните вводить страну"
      bind:value={citizenshipInput}
      on:input={() => { citizenshipCode = ''; }} 
      required
      autocomplete="off"
      aria-autocomplete="list"
      aria-controls="citizenship-list"
      class="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-[#0088cc] focus:border-[#0088cc]"
    />
    
    {#if citizenshipInput.length > 0 && !isCitizenshipSelected}
      <ul id="citizenship-list" class="absolute z-10 w-full bg-white border border-gray-300 rounded-b-md shadow-lg max-h-52 overflow-y-auto">
        {#each filteredCitizenshipCountries.slice(0, 5) as country (country.code)}
          <li on:mousedown|preventDefault={() => selectCitizenship(country)}
              tabindex="0"
              role="option"
              class="px-3 py-2 cursor-pointer hover:bg-blue-100 focus:bg-blue-100 transition-colors duration-150">
            {country.russianName} ({country.englishName})
          </li>
        {:else}
          {#if citizenshipInput.length > 0}
            <li class="px-3 py-2 text-gray-500 italic">Нет совпадений</li>
          {/if}
        {/each}
      </ul>
    {/if}
  </div>
  
  <button
    type="submit"
    disabled={!firstName || !lastName || !email || !isCitizenshipSelected}
    class="w-full py-2 bg-[#0088cc] text-white font-semibold rounded-md transition duration-150 hover:bg-[#0066a3] disabled:bg-gray-400 disabled:cursor-not-allowed"
  >
    Сохранить данные
  </button>
</form>