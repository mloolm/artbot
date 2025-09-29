<script>
    import { createEventDispatcher } from 'svelte';
    import { onDestroy } from 'svelte';

    // Получаем начальные данные работы (если это редактирование)
    export let work = {
        name: '',
        size: '',
        dimension: 'см'
    };

    // Генерируем уникальный ID для работы, чтобы управлять ей в списке
    const workId = Math.random(); 

    const dispatch = createEventDispatcher();
    
    // Единицы измерения
    const dimensions = ['см', 'мм', 'м'];

    // Отправляем событие 'update' при изменении любых данных
    function updateWork() {
        dispatch('update', {
            id: workId,
            ...work
        });
    }

    // Отправляем начальное состояние при монтировании
    onDestroy(() => {
        // Очистка или что-то еще, если потребуется
    });
</script>

<div class="p-4 bg-gray-50 border border-gray-200 rounded-lg space-y-3">
    <div class="text-right mb-2">
        
        
        <button 
            type="button" 
            on:click={() => dispatch('delete', workId)}
            class="text-red-500 hover:text-red-700 transition"
            title="Удалить работу"
        >
           Удалить работу ❌
        </button>
    </div>

    <div class="space-y-1">
        <label for="work-name-{workId}" class="block text-sm font-medium text-gray-700">Название работы</label>
        <input
            id="work-name-{workId}"
            type="text"
            placeholder="Например, 'Утро в горах'"
            bind:value={work.name}
            on:input={updateWork}
            required
            class="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
        />
    </div>

    <div class="flex space-x-3">
        <div class="space-y-1 flex-grow">
            <label for="work-size-{workId}" class="block text-sm font-medium text-gray-700">Размер (например, 44x33)</label>
            <input
                id="work-size-{workId}"
                type="text"
                placeholder="44x33"
                bind:value={work.size}
                on:input={updateWork}
                required
                class="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
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
                {#each dimensions as dim}
                    <option value={dim}>{dim}</option>
                {/each}
            </select>
        </div>
    </div>
</div>