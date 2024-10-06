import { apiUrl } from '@/api';

export const orderMixin = {
    methods: {
        async generateReport() {
            let response = await fetch(`${apiUrl}/reports`);
            if (this.statusCode == 200) {
                const url = window.URL.createObjectURL(new Blob([response]));
                const link = document.createElement('a');
                link.href = url;
                link.setAttribute('download', 'order.xlsx');
                document.body.appendChild(link);
                link.click();
            }
        },
    },
}
