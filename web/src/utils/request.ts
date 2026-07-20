const params = new URLSearchParams(window.location.search);

const api_url = params.get('api_url') ? (params.get('api_url') as string) : 'http://localhost:8000/api';
console.log("API URL:", api_url);

function getApiUrl(api: string) {
    const url = new URL(`/api/${api}`, api_url);
    return url;
}

export async function getApi(api: string, params: Record<string, string>, options?: object): Promise<any> {
    const url = getApiUrl(api);
    const searchParams = new URLSearchParams(params);
    url.search = searchParams.toString();
    const fetchOptions = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
        ...options,
    };
    const response = await fetch(url, fetchOptions);
    if (!response.ok) {
        throw new Error(`请求失败: ${response.status} ${response.statusText}`);
    };
    return await response.json();
}

