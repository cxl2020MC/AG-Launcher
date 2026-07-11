<script setup lang="ts" vapor>
import { watch } from 'vue'
import useEmblaCarousel from 'embla-carousel-vue'
import Autoplay from 'embla-carousel-autoplay'
// import { Icon } from "@iconify/vue";
import IconLeft from "~icons/fa7-solid/angle-left"
import IconRight from "~icons/fa7-solid/angle-right"

import type {Banners} from '@/type/banners'



const [slideshowRef, slideshowApi] = useEmblaCarousel({ loop: true }, [Autoplay()])

const scrollPrev = () => slideshowApi.value?.scrollPrev()
const scrollNext = () => slideshowApi.value?.scrollNext()

watch(
  slideshowApi,
  (api) => {
    if (!api) return
    api.plugins().autoplay?.play()
  },
  { immediate: true }
)

const props = defineProps<{
    imgs: {
        img: string;
        link: string;
    }[];
}>()
</script>

<template>
    <div class="slideshow">
        <div class="slideshow__viewport" ref="slideshowRef">
            <div class="slideshow__container">
                <template v-for="prop in props.imgs">
                    <a class="slideshow__slide" :href="prop.link" target="_blank">
                        <img class="" :src="prop.img">
                    </a>
                </template>
            </div>
        </div>

        <button class="slideshow__prev" @click="scrollPrev">
            <!-- <Icon icon="fa7-solid:angle-left" /> -->
            <IconLeft />
        </button>
        <button class="slideshow__next" @click="scrollNext">
            <!-- <Icon icon="fa7-solid:angle-right" /> -->
            <IconRight/>
        </button>
    </div>
</template>


<style scoped>
.slideshow {
    position: relative;
}

.slideshow__viewport {
    overflow: hidden;
}

.slideshow__container {
    display: flex;
    touch-action: pan-y pinch-zoom;
}

.slideshow__slide {
    flex: 0 0 100%;
    min-width: 0;
    height: 100%;
}

.slideshow__slide img {
    width: 100%;
    height: 100%;
    object-fit: contain;
}

.slideshow:hover button {
    opacity: 1;
}

button {
    color: #fff;
    background: none;
    border-style: none;
    font-size: 2rem;
    padding: 0;
    display: flex;
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    backdrop-filter: var(--blur);
    background: var(--blur-bg);
    opacity: 0;
    transition: .3s;
    cursor: pointer;
}

/* .slideshow__prev {
    left: 0;
    border-radius: 0 .5rem .5rem 0;
}

.slideshow__next {
    right: 0;
    border-radius: .5rem 0 0 .5rem;
} */

.slideshow__prev {
    left: .5rem;
    border-radius: 999rem;
}

.slideshow__next {
    right: .5rem;
    border-radius: 999rem;
}
</style>