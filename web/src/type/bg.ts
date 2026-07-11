export type Backgrounds = Background[];

export interface Background {
    id: string;
    background: {
        url: string;
        link: string;
        login_state_in_link: boolean;
    };
    icon: {
        url: string;
        hover_url: string;
        link: string;
        login_state_in_link: boolean;
        md5: string;
        size: number;
    };
    video: {
        url: string;
        size: number;
    };
    theme: {
        url: string;
        link: string;
        login_state_in_link: boolean;
    };
    type: "BACKGROUND_TYPE_VIDEO" | "BACKGROUND_TYPE_UNSPECIFIED"
}


