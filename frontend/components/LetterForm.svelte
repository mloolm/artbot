<script>
    import { createEventDispatcher } from 'svelte';
    import WorkItem from './WorkItem.svelte'; // Компонент одной работы
    
    const dispatch = createEventDispatcher();

    // Импортируем данные о странах и создаем карту для поиска
    import countryData from '../data/countries.json'; 
    const countries = Object.entries(countryData).map(([code, names]) => ({
        code: code,
        englishName: names[0],  
        russianName: names[1],  
        // 5-й столбец (индекс 4) теперь важен для country_to
        valueCountryTo: names[4]    
    }));
    const countryMap = new Map(countries.map(c => [c.code, c]));

    import typeData from '../data/types.json';
    const typeDataVals = Object.values(typeData); 
    const default_item_type = typeDataVals[0][0];
    const default_item_type_rod = typeDataVals[0][1];
    
    import reasonData from '../data/reasons.json';
    const reasonDataVals = Object.values(reasonData); 
    const default_reason = reasonDataVals[0][1];


    import mediumData from '../data/mediums.json';
    const mediumDataVals = Object.values(mediumData); 
    const default_medium = mediumDataVals[0];


    import mediumBaseData from '../data/mediums_base.json';
    const mediumBaseDataVals = Object.values(mediumBaseData); 
    const default_medium_base = mediumBaseDataVals[0];


    // --- ФОРМА ИЗ PISMA (Письма) ---
    export let countryToInput = ''; 
    export let countryToCode = ''; 

    function getEmptyWorkObject()
    {
        return { 
            id: Date.now(), 
            name: '', 
            size: '', 
            dimension: 'სმ',
            item_type:default_item_type,
            item_type_rod:default_item_type_rod,
            reason:default_reason,
            medium: default_medium,
            medium_base:default_medium_base
        }
    }
    
    // Список работ (инициализируем одной пустой работой)
    export let items = [
        getEmptyWorkObject()
    ];

    // --- ЛОГИКА COUNTRY_TO ---
    
    function filterCountries(input) {
        if (!input) return [];
        const searchLower = input.toLowerCase();
        return countries.filter(country =>
            country.russianName.toLowerCase().includes(searchLower) || 
            country.englishName.toLowerCase().includes(searchLower)   
        );
    }
    
    $: filteredCountryToCountries = filterCountries(countryToInput);
    $: isCountryToSelected = countryToCode && countryMap.get(countryToCode)?.russianName === countryToInput;

    function selectCountryTo(country) {
        countryToInput = country.russianName; 
        countryToCode = country.code;
    }

    // --- ЛОГИКА РАБОТ (ITEMS) ---
    
    function addWork() {
        items = [...items, getEmptyWorkObject()];
    }

    function handleWorkUpdate(event) {
        const updatedWork = event.detail;
        items = items.map(item => 
            item.id === updatedWork.id ? { ...item, ...updatedWork } : item
        );
    }

    function handleWorkDelete(event) {
        const idToDelete = event.detail;
        console.log(items, idToDelete);
        items = items.filter(item => item.id !== idToDelete);
    }

    // --- ОБРАБОТЧИК ОТПРАВКИ (СБОРКА ДАННЫХ) ---
    
    function handleSubmit() {
        // Проверка: все ли работы имеют название и размер
        const isValid = items.every(item => item.name && item.size);

        if (!isValid) {
            alert("Пожалуйста, заполните поля 'Название работы' и 'Размер' для всех работ.");
            return;
        }

        // Находим финальное значение 5-го столбца
        const countryToValue = countryMap.get(countryToCode)?.valueCountryTo;

        // Отправляем событие 'submit' с данными формы
        dispatch('submit', { 
            countryToCode,
            countryToValue,
            items: items.map(item => ({
                name: item.name,
                size: item.size,
                dimension: item.dimension,
                reason: item.reason, 
                item_type: item.item_type,
                item_type_rod: item.item_type_rod,
                medium: item.medium,
                medium_base: item.medium_base
            }))
        });
    }
</script>

<form on:submit|preventDefault={handleSubmit} class="space-y-6">

    <div class="p-5 bg-white shadow-md rounded-lg space-y-4">
        <div class="space-y-1 relative">
            <label for="countryTo" class="block font-medium text-gray-700">
                Куда отправляются (вывозятся) работы
            </label>
            <input
                id="countryTo"
                type="text"
                placeholder="Начните вводить страну"
                bind:value={countryToInput}
                on:input={() => { countryToCode = ''; }} 
                required
                autocomplete="off"
                aria-autocomplete="list"
                class="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
            />
            
            {#if countryToInput.length > 0 && !isCountryToSelected}
                <ul class="absolute z-10 w-full bg-white border border-gray-300 rounded-b-md shadow-lg max-h-52 overflow-y-auto">
                    {#each filteredCountryToCountries.slice(0, 5) as country (country.code)}
                        <li on:mousedown|preventDefault={() => selectCountryTo(country)}
                            class="px-3 py-2 cursor-pointer hover:bg-blue-100">
                            {country.russianName} ({country.englishName})
                        </li>
                    {:else}
                        {#if countryToInput.length > 0}
                            <li class="px-3 py-2 text-gray-500 italic">Нет совпадений</li>
                        {/if}
                    {/each}
                </ul>
            {/if}
        </div>
    </div>

    <div class="p-5 bg-white shadow-md rounded-lg space-y-4">
        <h3 class="text-lg font-bold text-gray-800 border-b pb-2">Список работ</h3>

        <div class="space-y-4">
            {#each items as item (item.id)}
                <WorkItem 
                work={item} 
                workId={item.id} 
                typeData={typeData}
                reasonData={reasonData}
                mediumData={mediumData}
                mediumBaseData={mediumBaseData}
                on:update={handleWorkUpdate} on:delete={handleWorkDelete} />
            {/each}
        </div>

        <button 
            type="button" 
            on:click={addWork}
            class="w-full py-2 border border-blue-500 text-blue-500 font-semibold rounded-md transition hover:bg-blue-50"
        >
            + Добавить работу
        </button>
    </div>

    <button
        type="submit"
        disabled={!countryToCode || items.length === 0}
        class="w-full py-3 bg-[#0088cc] text-white font-semibold rounded-md transition duration-150 hover:bg-[#0066a3] disabled:bg-gray-400 disabled:cursor-not-allowed"
    >
        Сгенерировать Письмо
    </button>
</form>