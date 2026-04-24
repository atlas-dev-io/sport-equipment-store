<template>
  <div ref="chartRef" class="chart-container"></div>
</template>

<script setup lang="ts">
import { nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import * as echarts from 'echarts'
import type { ECharts, EChartsOption } from 'echarts'

const props = defineProps<{
  option: EChartsOption
  height?: string
}>()

const chartRef = ref<HTMLElement | null>(null)
let chartInstance: ECharts | null = null

function initChart() {
  if (!chartRef.value) return

  if (!chartInstance) {
    chartInstance = echarts.init(chartRef.value)
  }

  chartInstance.setOption(props.option, true)
}

function resizeChart() {
  chartInstance?.resize()
}

watch(
  () => props.option,
  async () => {
    await nextTick()
    initChart()
  },
  { deep: true },
)

onMounted(() => {
  if (chartRef.value && props.height) {
    chartRef.value.style.height = props.height
  }
  initChart()
  window.addEventListener('resize', resizeChart)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', resizeChart)
  chartInstance?.dispose()
  chartInstance = null
})
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 320px;
}
</style>