import { apiUrl } from '@/api';

export const orderMixin = {
    methods: {
        async generateReport(metric_type) {
            try {
                const response = await fetch(`${apiUrl}/reports/${metric_type}`);
                // Проверяем успешность ответа
                if (response.ok) {  // Правильная проверка на статус ответа
                    const blob = await response.blob(); // Извлекаем данные в виде Blob
                    const url = window.URL.createObjectURL(blob);
                    const link = document.createElement('a');
                    link.href = url;
                    link.setAttribute('download', 'report.xlsx');
                    document.body.appendChild(link);
                    link.click();
                    link.remove(); // Удаляем элемент после клика
                    window.URL.revokeObjectURL(url); // Освобождаем память
                } else {
                    console.error('Ошибка при загрузке отчета:', response.status, response.statusText);
                }
            } catch (error) {
                console.error('Ошибка при генерации отчета:', error);
            }
        },
    },
};
