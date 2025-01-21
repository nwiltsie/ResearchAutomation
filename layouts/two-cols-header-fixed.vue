<!--
  Usage:
```md
---
layout: two-cols-header-fixed
---
This spans both
::left::
# Left
This shows on the left
::right::
# Right
This shows on the right
::bottom::
This shows at the bottom, aligned to the end (bottom) of the grid
```
-->

<script setup lang="ts">
const props = defineProps({
  class: {
    type: String,
  },
  layoutClass: {
    type: String,
  },
})
</script>

<template>
  <div class="slidev-layout two-cols-header-fixed w-full h-full" :class="layoutClass">
    <div class="col-header">
      <slot name="header" />
    </div>
    <div class="col-left" :class="props.class">
      <slot name="left" />
    </div>
    <div class="col-right" :class="props.class">
      <slot name="right" />
    </div>
    <div class="col-bottom" :class="props.class">
      <slot name="bottom" />
    </div>
  </div>
</template>

<style scoped>
.two-cols-header-fixed {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: repeat(4, 1fr);
}

.col-header { grid-area: 1 / 1 / 2 / 3; }
.col-left { grid-area: 2 / 1 / 3 / 2; }
.col-center { grid-area: 2 / 2 / 3 / 3; }
.col-bottom {
  grid-area: 3 / 1 / 4 / 3;
}
</style>
