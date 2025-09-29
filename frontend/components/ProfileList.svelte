<script>
    import { navigate } from 'svelte-routing';
    import { onMount } from 'svelte';

    let profiles = [];
    const STORAGE_KEY = 'userProfiles';

    onMount(loadProfiles);

    function loadProfiles() {
        try {
            const storedProfiles = localStorage.getItem(STORAGE_KEY);
            if (storedProfiles) {
                profiles = JSON.parse(storedProfiles);
            }
        } catch (e) {
            console.error("Ошибка загрузки профилей:", e);
        }
    }

    function saveProfiles() {
        try {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(profiles));
        } catch (e) {
            console.error("Ошибка сохранения профилей:", e);
        }
    }

    function handleEdit(id) {
        navigate(`/profile/edit/${id}`);
    }

    function handleDelete(id) {
        if (confirm('Вы уверены, что хотите удалить этот профиль?')) {
            profiles = profiles.filter(p => p.id !== id);
            saveProfiles();
        }
    }

    function handleMakeLetter(id){
        navigate(`/letter/${id}`);
    }

    // Вспомогательная функция для получения русского названия страны по коду
    // (Подразумевается, что countryData доступен, или его нужно импортировать)
    import countryData from '../data/countries.json'; 
    import Profile from '../src/Profile.svelte';
    const countryMap = new Map(Object.entries(countryData));

    function getCountryName(code) {
        if (!code) return 'Не указано';
        const names = countryMap.get(code);
        return names ? names[1] : code; // Возвращаем русское название (индекс 1)
    }

</script>

<div class="w-full max-w-md space-y-4">
    <h2 class="text-2xl font-bold text-gray-800 text-center">
        Сохраненные профили ({profiles.length})
    </h2>

    {#if profiles.length === 0}
        <div class="p-4 bg-yellow-100 text-yellow-800 rounded-lg text-center">
            У вас пока нет сохраненных профилей.
        </div>
    {:else}
        <ul class="space-y-3">
            {#each profiles as profile (profile.id)}
               <li class="bg-white p-4 rounded-lg shadow-md border-l-4 border-[#0088cc] space-y-3">
                    
                    <div class="flex justify-between items-center w-full"> 
                        <div class=""> 
                            <p class="text-lg font-semibold text-gray-900">
                                {profile.firstName} {profile.lastName}
                            </p>
                            <p class="text-sm text-gray-600">
                                Гражданство: {getCountryName(profile.citizenshipCode)}
                            </p>
                        </div>
                        
                        <div class="flex space-x-2">
                            <button 
                                on:click={() => handleEdit(profile.id)}
                                class="p-2 inline-block text-sm bg-blue-500 text-white rounded-full hover:bg-blue-600 transition"
                                title="Редактировать"
                            >
                                ✏️
                            </button>
                            <button 
                                on:click={() => handleDelete(profile.id)}
                                class="p-2 inline-block ml-3 text-sm bg-white-500 text-white rounded-full hover:bg-red-100 transition"
                                title="Удалить"
                            >
                                ❌
                            </button>
                        </div>
                    </div>
                    
                    <div class=py-2>
                    <button
                        on:click={() => handleMakeLetter(profile.id)}
                        class="w-full text-white px-6 py-3 hover:bg-blue-600 transition bg-[#0088cc]"
                        title="Сформировать письмо"
                    >
                        Сформировать письмо
                    </button>    

                    </div>
                </li>
            {/each}
        </ul>
    {/if}
</div>