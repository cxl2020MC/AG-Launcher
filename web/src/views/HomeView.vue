<script setup lang="ts" vapor>
import { ref, computed } from 'vue';
import SlideShow from '@/components/SlideShow.vue';
import { useGameStore } from '@/stores/game'
import { getApi } from '@/utils/request'


const game_data = ref<Record<string, any> | null>(null)

getApi('game_info', { area: 'cn', launcher: '国服', game_biz: 'hk4e_cn' }).then((data) => {
    game_data.value = data
})

const game_icon = computed(() => game_data.value?.display?.icon?.url)
console.log(game_data.value)

const bg_datas = useGameStore()


const bg_num = ref(0)
const bg_data = ref(bg_datas[bg_num.value])
const bg_video_play = ref(true)

const posts_type = ref("POST_TYPE_ACTIVITY")
const post_data = [
    {
        "id": "S8XxOTXy47",
        "type": "POST_TYPE_ACTIVITY",
        "title": "「当我们抬头看月亮」「月之八」合影活动开启，参与必得评论装扮",
        "link": "https://www.miyoushe.com/ys/article/76351908",
        "date": "07/02",
        "login_state_in_link": false,
        "i18n_identifier": ""
    },
    {
        "id": "PddVdkI8jo",
        "type": "POST_TYPE_ACTIVITY",
        "title": "【有奖活动】「月之八」版本第一期话题活动开启~",
        "link": "https://www.miyoushe.com/ys/article/76351734",
        "date": "07/01",
        "login_state_in_link": false,
        "i18n_identifier": ""
    },
    {
        "id": "K3WgzO0kuC",
        "type": "POST_TYPE_ACTIVITY",
        "title": "【有奖活动】「镜水析谬」桑多涅绘画征集活动开启！",
        "link": "https://act.mihoyo.com/ys/event/doujin-collection/index.html?id=ea202606181648058769&act_id=ea202606181648058769&game_biz=hk4e&mhy_presentation_style=fullscreen",
        "date": "06/22",
        "login_state_in_link": false,
        "i18n_identifier": ""
    },
    {
        "id": "W0iXgX2wDh",
        "type": "POST_TYPE_ANNOUNCE",
        "title": "「镜中的茶宴」祈愿：「镜水析谬·桑多涅(冰)」概率UP！",
        "link": "https://www.miyoushe.com/ys/article/76308879",
        "date": "06/29",
        "login_state_in_link": false,
        "i18n_identifier": ""
    },
    {
        "id": "J1zcdfNU1Z",
        "type": "POST_TYPE_ANNOUNCE",
        "title": "「星边夜语」祈愿：「白星黑曜·茜特菈莉(冰)」概率UP！",
        "link": "https://www.miyoushe.com/ys/article/76308876",
        "date": "06/29",
        "login_state_in_link": false,
        "i18n_identifier": ""
    },
    {
        "id": "By6Quzmp4i",
        "type": "POST_TYPE_ANNOUNCE",
        "title": "「米哈游启动器」常见问题说明",
        "link": "https://www.miyoushe.com/ys/article/53085953",
        "date": "05/22",
        "login_state_in_link": false,
        "i18n_identifier": ""
    },
    {
        "id": "wH8qhnQ8EP",
        "type": "POST_TYPE_INFO",
        "title": "《原神》过场动画-「安眠于众水」",
        "link": "https://www.miyoushe.com/ys/article/76552927",
        "date": "07/09",
        "login_state_in_link": false,
        "i18n_identifier": ""
    },
    {
        "id": "dLI1fAMpIE",
        "type": "POST_TYPE_INFO",
        "title": "《原神》剧情PV-「何物映自身于镜水」",
        "link": "https://www.miyoushe.com/ys/article/76528070",
        "date": "07/08",
        "login_state_in_link": false,
        "i18n_identifier": ""
    },
    {
        "id": "mj4UnP6PLI",
        "type": "POST_TYPE_INFO",
        "title": "在星海间，再见吧",
        "link": "https://www.miyoushe.com/ys/article/76461765",
        "date": "07/05",
        "login_state_in_link": false,
        "i18n_identifier": ""
    }
]

const imgs = [
    {
        img: "https://launcher-webstatic.mihoyo.com/launcher-public/2026/07/09/eca3d692600ea2cdadcd4e31061a3e78_8469405147442238671.jpg",
        link: "https://www.miyoushe.com/ys/article/76036597"
    },
    {
        img: "https://launcher-webstatic.mihoyo.com/launcher-public/2026/07/05/b8a359f1f020526eb7a07c162d5634d3_6104488516091645661.jpg",
        link: "https://www.miyoushe.com/ys/article/76036597"
    },
    {
        img: "https://launcher-webstatic.mihoyo.com/launcher-public/2026/07/09/d4746c05357b3cedfa3850545ca83c8a_3805866506083704608.png",
        link: "https://www.miyoushe.com/ys/article/76036597"
    }
]
</script>

<template>
    <div class="main">
        <div class="background-div">
            <template v-if="bg_data">
                <template v-if="bg_data.type === 'BACKGROUND_TYPE_VIDEO' && bg_video_play">
                    <video class="background" :src="bg_data.video.url" :poster="bg_data.background.url" autoplay loop
                        muted></video>
                    <img class="background" :src="bg_data.theme.url">
                </template>
                <template v-else-if="bg_data.type === 'BACKGROUND_TYPE_UNSPECIFIED'">
                    <img class="background" :src="bg_data.background.url">
                </template>
            </template>
        </div>
        <!-- <video class="background" src="https://launcher-webstatic.mihoyo.com/launcher-public/2026/06/10/baf3e7fb8f3d0465eaf9f680d168ab3a_4670576832169094293.webm" autoplay loop></video> -->
        <!-- <img src="https://launcher-webstatic.mihoyo.com/launcher-public/2026/05/26/30b6f666378d012b8763e224f4c96656_440171036365066232.webp" alt="" class="background"> -->
        <div class="left-menu">
            <img class="game-icon" :src="game_icon" alt="">
            <div class="game-menus">

            </div>
        </div>
        <div class="content">
            <div class="backgroud-swicher">
                <div class="background-swicher-item"></div>
            </div>
            <div class="left-aside">
                <div class="aside-bg-icon-div">
                    <img class="aside-bg-icon" v-if="bg_data" :src="bg_data.icon.url" />
                    <img class="aside-bg-icon-hover" v-if="bg_data" :src="bg_data.icon.hover_url" />
                </div>

                <aside class="aside">
                    <SlideShow class="slideshow" :imgs="imgs"></SlideShow>
                    <div class="activity">
                        <div class="activity-tabs">
                            <div :class="`activity-tab-item ${posts_type === 'POST_TYPE_ACTIVITY' ? 'active' : ''}`"
                                @click="posts_type = 'POST_TYPE_ACTIVITY'">活动</div>
                            <div :class="`activity-tab-item ${posts_type === 'POST_TYPE_ANNOUNCE' ? 'active' : ''}`"
                                @click="posts_type = 'POST_TYPE_ANNOUNCE'">公告</div>
                        </div>
                        <div class="activity-posts">
                            <template v-for="post in post_data" :key="post.id">
                                <template v-if="post.type === posts_type">
                                    <p>{{ post.title }}</p>
                                </template>
                            </template>
                        </div>
                    </div>
                </aside>
            </div>
        </div>
    </div>

</template>

<style scoped>
.main {
    aspect-ratio: 16 / 9;
    position: relative;
    display: flex;
}

.left-menu {
    height: 100%;
    width: 5%;
    backdrop-filter: var(--blur);
    background: var(--blur-bg);
    padding: .5em;
}

.left-menu .game-icon {
    width: 100%;
    border-radius: .5em;
}

.content {
    position: relative;
    height: 100%;
    flex: 1 1 auto
}

.background-div {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    z-index: -1;
}

.background {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
}

.left-aside {
    position: absolute;
    bottom: 0;
    left: 0;
    padding: 5%;
}

.aside {
    width: 20em;
    background: var(--blur-bg);
    backdrop-filter: var(--blur);
    overflow: hidden;
    border-radius: 1em;
}

.aside-bg-icon-div {
    width: 35%;
}

.aside-bg-icon,
.aside-bg-icon-hover {
    width: 100%;
}

.aside-bg-icon-div:hover .aside-bg-icon,
.aside-bg-icon-hover {
    display: none;
}

.aside-bg-icon-div:hover .aside-bg-icon-hover {
    display: block;
}

.aside .slideshow {
    width: 100%;
    aspect-ratio: 69/32;
}

.aside .activity {
    padding: 0.5em;
}

.aside .activity .activity-tabs {
    display: flex;
    gap: 1em;
    font-weight: bold;
    cursor: pointer;
}

.aside .activity .activity-tabs .activity-tab-item.active::after {
    display: block;
    width: 100%;
    height: .1em;
    content: '';
    background: #fff;
    border-radius: 9999em;

}

.aside .activity .activity-posts {
    max-height: 4em;
    margin-top: 0.5em;
    overflow: auto;
    scrollbar-width: thin;
    scrollbar-color: var(--scrollbar-color) transparent;
}

.aside .activity .activity-posts p {
    margin: 0;
    width: 100%;
    text-overflow: ellipsis;
    /* 超出部分显示省略号 */
    overflow: hidden;
    /* 隐藏超出部分 */
    white-space: nowrap;
    /* 禁止换行 */
}
</style>