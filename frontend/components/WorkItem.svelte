<script>
    import { createEventDispatcher } from 'svelte';
    import { onDestroy } from 'svelte';

    export let workId; 
    export let work;
    export let typeData;
    export let reasonData;
    export let mediumData;
    export let mediumBaseData;

    const russianTypes = Object.keys(typeData);

    // Вспомогательная функция для получения грузинского названия 
    function getGeorgianDimension(code) {
        return dimensionMap[code] || code;
    }

    function handleTypeChange(event) {
        // event.target.value будет русским ключом (например, "картина")
        const selectedRussianType = event.target.value; 
        
        // Находим массив грузинских падежей [И.п., Р.п.]
        const [nominative, genitive] = typeData[selectedRussianType];

        // Обновляем два поля в work
        work.item_type = nominative; // "ნახატი" (для письма)
        work.item_type_rod = genitive; // "ნახატის" (для письма)

        // Вызываем родительский update
        updateWork();
    }

    const dispatch = createEventDispatcher();
    
    // Карта для отображения грузинских названий
     const dimensionMap = {
        'см': 'სმ',
        'мм': 'მმ',
        'м': 'მ'
    };

    function updateWork() {
        dispatch('update', {
            id: workId,
            ...work
        });
    }

    onDestroy(() => {
        // Очистка или что-то еще, если потребуется
    });
</script>

<div class="p-4 bg-gray-50 border border-gray-200 rounded-lg space-y-3">
     <div class="text-right pb-4">
        <button 
            type="button" 
            on:click={() => dispatch('delete', workId)} 
            class="text-red-500 hover:text-red-700 transition"
            title="Удалить работу"
        >
           Удалить работу ❌
        </button>
    </div>

    <div class="w-full space-y-1">
        <label for="work-type-{workId}" class="block text-sm font-medium text-gray-700">Тип работы</label>
        <select
            id="work-type-{workId}"
            
            on:change={handleTypeChange}
            class="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 bg-white"
        >
            {#each russianTypes as rusType}
                <option 
                    value={rusType}
                    selected={rusType === Object.keys(typeData).find(key => typeData[key][0] === work.item_type)}
                >
                    {rusType}
                </option>
            {/each}
        </select>
    </div>

    <div class="w-full">
        <label for="work-name-{workId}" class="block text-sm font-medium text-gray-700">Название на грузинском</label>
        <input
            id="work-name-{workId}" 
            bind:value={work.name}
            on:change={updateWork}
            placeholder=""
            class="w-full block border border-gray-300 rounded-md px-2 py-1"
            >
    </div>
    <div class="flex space-x-3">
        <div class="space-y-1 flex-grow">
            <label for="work-size-{workId}" class="block text-sm font-medium text-gray-700">Размер</label>
            <input
                id="work-size-{workId}"
                type="text"
                placeholder="30x40 или 20x20x10"
                bind:value={work.size}
                on:input={updateWork}
                required
                class="w-full p-2 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-blue-500"
            />
        </div>
        <div class="space-y-1 w-24">
            <label for="work-dim-{workId}" class="block text-sm font-medium text-gray-700">Ед. изм.</label>
            <select
                id="work-dim-{workId}"
                bind:value={work.dimension}
                on:change={updateWork}
                class="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 bg-white"
            >
                 {#each Object.entries(dimensionMap) as [dimKey, dimValue]}
                    <option value={dimValue}>{dimKey}</option> 
                {/each}
            </select>
        </div>
    </div>
    <div class="flex space-x-3">
        <div class="space-y-1 flex-grow">
            <label for="work-medium-{workId}" class="block text-sm font-medium text-gray-700">Материал / Техника</label>
            <select
                id="work-medium-{workId}"
                bind:value={work.medium}
                on:change={updateWork}
                class="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 bg-white"
            >
                {#each Object.entries(mediumData) as [russianText, georgianValue]}
                    <option value={georgianValue}>
                        {russianText}
                    </option>
                {/each}
            </select>
        </div>
        
        <div class="space-y-1 flex-grow">
            <label for="work-base-{workId}" class="block text-sm font-medium text-gray-700">Основа</label>
            <select
                id="work-base-{workId}"
                bind:value={work.medium_base}
                on:change={updateWork}
                class="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 bg-white"
            >
                {#each Object.entries(mediumBaseData) as [russianText, georgianValue]}
                    <option value={georgianValue}>
                        {russianText}
                    </option>
                {/each}
            </select>
        </div>
    </div>
     <div class="w-full space-y-1">
        <label for="work-reason-{workId}" class="block text-sm font-medium text-gray-700">Откуда у вас эта работа?</label>
        <select
            id="work-reason-{workId}"
            bind:value={work.reason}
            on:change={updateWork}
            class="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 bg-white"
        >
            {#each reasonData as [russianText, georgianValue]}
                <option value={georgianValue}>
                    {russianText}
                </option>
            {/each}
        </select>
    </div>
</div>