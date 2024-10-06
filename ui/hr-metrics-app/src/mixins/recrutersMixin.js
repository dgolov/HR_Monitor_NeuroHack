import { apiUrl } from '@/api';

export const recrutersMixin = {
    data() {
        return {
            recruters: [],
            itemRecruter: null,
        }
    },
    methods: {
        async fetchRecruterst() {
            try {
                const response = await fetch(`${apiUrl}/users/?role=recruiter`);
                if (!response.ok) {
                    throw new Error(`Ошибка сети: ${response.statusText}`);
                }
                this.recruters = await response.json();
                this.itemRecruter = this.recruters[0]
            } catch (error) {
                console.error('Ошибка при загрузке рекрутеров:', error);
            }
        },
    },
}
