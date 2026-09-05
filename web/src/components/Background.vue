<script setup lang="ts">
import { ref } from 'vue'
import { useGameBackgroundStore } from '@/stores/game'

const bg_datas = useGameBackgroundStore()


const bg_num = ref(0)
const bg_data = ref(bg_datas[bg_num.value])
const bg_video_play = ref(true)

</script>

<template>
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
</template>