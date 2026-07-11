
export type Banners = Banner[];

export interface Banner {
    id: string;
    image: {
        url: string;
        link: string;
        login_state_in_link: boolean;
    }
    i18n_identifier: string;
}
