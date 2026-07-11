<script setup lang="ts" vapor>
</script>

<template>
  <header>
    <nav>
    </nav>
  </header>
  <main>
    <router-view />
  </main>
</template>


<style scoped></style>

<style>
body {
  margin: 0;
  color: #fff;
}

* {
  box-sizing: border-box;

}

:root {
  --blur: blur(1rem);
  --blur-bg: rgb(30 30 30 / 30%);
  --scrollbar-color: rgb(255 255 255 / 50%);
}

:root {
  color-scheme: light dark;
}

body {
  width: 100vw;
  height: 100vh;
  overflow: hidden; /* 关键：移除滚动条，保证“最大”就是视口大小 */
  
  /* 使用 Flex 让 div 居中（非必须，但视觉效果最佳） */
  display: flex;
  justify-content: center;
  align-items: center;
  background: transparent;
}

main {
  /* 核心宽高比 */
  aspect-ratio: 16 / 9;
  
  /* 
    核心尺寸逻辑：
    宽度取“视口宽度”和“按高度换算出的宽度”中的较小值
    高度由 aspect-ratio 自动推导，保证比例不失真
  */
  width: min(100vw, calc(100vh * 16 / 9));
  height: auto; /* 让 aspect-ratio 接管高度 */
}
</style>
