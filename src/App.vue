<script setup lang="ts">
import { getData, getDataByIndex } from "./apis/data.ts";
import { ref, onMounted, nextTick } from "vue";

const total = ref<number>(0);
const row = ref<number>(0);
const col = ref<number>(0);

const matrix = ref<number[][][]>([]);

const containerRef = ref<HTMLDivElement>();
const canvas = ref<HTMLCanvasElement>();

const percentageRef = ref<number>(0);
const loadMatrix = async () => {
  let index = 0;
  while (index < total.value) {
    matrix.value?.push(await getDataByIndex(index));
    index += 1;
    percentageRef.value = Number((index * 100 / total.value).toFixed(0));
  }
  loading.value = false;
};

let page = 0;
const colors = [
    "#F8FAFC",
    "#F9FAFB",
    "#FAFAFA",
    "#FAFAFA",
    "#FAFAF9",
    "#FEF2F2",
    "#FFF7ED",
    "#FFFBED",
    "#FEFCEB",
    "#F7FEE7",
    "#F0FDF4",
    "#ECFDF5",
    "#F0FDFA",
    "#ECFEFF",
    "#F0F9FF",
    "#EFF6FF",
    "#EEF2FF",
    "#F5F3FF",
    "#FAF5FF",
    "#FDF4FF",
    "#FDF2F8",
    "#FFF1F2"
];
const bgs = [
  "#334155",
  "#374151",
  "#3F3F46",
  "#404040",
  "#334155",
  "#374151",
  "#3F3F46",
  "#404040",
  "#334155",
  "#374151",
  "#3F3F46",
  "#404040",
  "#334155",
  "#374151",
  "#3F3F46",
  "#404040",
  "#334155",
  "#374151",
  "#3F3F46",
  "#404040",
  "#334155",
  "#374151"
];
const loading = ref<boolean>(true)
const context = ref<CanvasRenderingContext2D>()
const animation = (index: number) => {
  context.value?.clearRect(0, 0, col.value * 5, row.value * 5)
  for (let r = 0; r < row.value; r++) {
    for (let c = 0; c < col.value; c++) {
      const randomKernel = Math.round(Math.random() * colors.length);
      if (matrix.value![index][r][c] == 0) {
        context.value!.fillStyle = colors[randomKernel];
        context.value!.fillRect(r * 5, c * 5, 5, 5);
      } else {
        context.value!.fillStyle = bgs[randomKernel];
        context.value!.fillRect(r * 5, c * 5, 5, 5);
      }
    }
  }

  page += 1
  if (page >= total.value) return
  requestAnimationFrame(() => animation(page))
}

onMounted(async () => {
  const data = await getData();
  total.value = data.total;
  row.value = data.row;
  col.value = data.col;

  console.log("正在加载数据")
  await loadMatrix();
  console.log("数据加载完毕", matrix.value)

  canvas.value = document.createElement("canvas");
  canvas.value.width = col.value * 5;
  canvas.value.height = row.value * 5;
  canvas.value.style.transform = "rotate(90deg)";

  context.value = canvas.value?.getContext("2d")!;
  context.value.font = "bold 5px serif"

  containerRef.value!.appendChild(canvas.value);

  await nextTick(() => {
    animation(page)
  });
});
</script>

<template>
  <n-space>
    <n-space v-if="loading">
      <n-progress type="circle" :percentage="percentageRef"></n-progress>
    </n-space>
    <n-space>
      <div ref="containerRef"></div>
    </n-space>
  </n-space>
</template>

<style scoped></style>
