import { defineStore } from 'pinia'
import type { Backgrounds } from '@/type/bg'


const bg_data_raw: Backgrounds = [
    {
        "id": "d7eCRqQwNc",
        "background": {
            "url": "https://launcher-webstatic.mihoyo.com/launcher-public/2026/07/06/2027860169a82faddcef8879b30f51b7_1360278772900840591.webp",
            "link": "",
            "login_state_in_link": false
        },
        "icon": {
            "url": "https://launcher-webstatic.mihoyo.com/launcher-public/2026/06/16/0e654b12d12e37ee3923e1240c209266_5879432368107123917.png",
            "hover_url": "https://launcher-webstatic.mihoyo.com/launcher-public/2026/06/16/6983dda28b0351055771e65282c53096_1670070773872150550.png",
            "link": "https://webstatic.mihoyo.com/ys/event/e20210601blue_post/vert.html?page_sn=026e946ecbc54a3d&bbs_presentation_style=fullscreen&utm_source=game&utm_medium=ys&utm_campaign=bt",
            "login_state_in_link": false,
            "md5": "",
            "size": 0
        },
        "video": {
            "url": "https://launcher-webstatic.mihoyo.com/launcher-public/2026/07/06/f5056f9c9bd0f95f0c08a6bf2abd0bb5_131367125454112694.webm",
            "size": 0
        },
        "theme": {
            "url": "https://launcher-webstatic.mihoyo.com/launcher-public/2026/06/16/e777eec6071dc60b5ee0fcb2e86283c0_4600941239787533419.webp",
            "link": "",
            "login_state_in_link": false
        },
        "type": "BACKGROUND_TYPE_VIDEO"
    },
    {
        "id": "Lpbk6DFGXh",
        "background": {
            "url": "https://launcher-webstatic.mihoyo.com/launcher-public/2026/06/17/3d16cc14b63d99a99cc69631183782a3_485812170769646437.webp",
            "link": "",
            "login_state_in_link": false
        },
        "icon": {
            "url": "https://launcher-webstatic.mihoyo.com/launcher-public/2026/06/17/0e654b12d12e37ee3923e1240c209266_7806434847917836055.png",
            "hover_url": "https://launcher-webstatic.mihoyo.com/launcher-public/2026/06/17/6983dda28b0351055771e65282c53096_4524405510881677906.png",
            "link": "https://webstatic.mihoyo.com/ys/event/e20210601blue_post/vert.html?page_sn=026e946ecbc54a3d&bbs_presentation_style=fullscreen&utm_source=game&utm_medium=ys&utm_campaign=bt",
            "login_state_in_link": false,
            "md5": "",
            "size": 0
        },
        "video": {
            "url": "",
            "size": 0
        },
        "theme": {
            "url": "",
            "link": "",
            "login_state_in_link": false
        },
        "type": "BACKGROUND_TYPE_UNSPECIFIED"
    },
    {
        "id": "4zT14tpFYi",
        "background": {
            "url": "https://launcher-webstatic.mihoyo.com/launcher-public/2026/06/29/cd14d9b6f5b6257c81ef4c7b6b25e2e0_800171892832315697.webp",
            "link": "",
            "login_state_in_link": false
        },
        "icon": {
            "url": "https://launcher-webstatic.mihoyo.com/launcher-public/2026/03/24/78243e37d17b1cd9d7f5523ddea73ab9_1430467952422516445.png",
            "hover_url": "https://launcher-webstatic.mihoyo.com/launcher-public/2026/01/08/6983dda28b0351055771e65282c53096_4636696950798100483.png",
            "link": "https://webstatic.mihoyo.com/ys/event/e20210601blue_post/vert.html?page_sn=026e946ecbc54a3d&bbs_presentation_style=fullscreen&utm_source=game&utm_medium=ys&utm_campaign=bt",
            "login_state_in_link": false,
            "md5": "",
            "size": 0
        },
        "video": {
            "url": "",
            "size": 0
        },
        "theme": {
            "url": "",
            "link": "",
            "login_state_in_link": false
        },
        "type": "BACKGROUND_TYPE_UNSPECIFIED"
    }
]

export const useGameStore = defineStore('game-bg', {
    state: (): typeof bg_data_raw => (bg_data_raw),
})