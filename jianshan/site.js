'use strict';
const previews = {
  overview: {src:'./assets/overview.png', alt:'见山总览：展示合成资产总额、资产分布与快照趋势'},
  assets: {src:'./assets/assets.png', alt:'见山资产页：分类维护多币种资产，图片中均为演示数据'},
  expenses: {src:'./assets/expenses.png', alt:'见山消费账本：按月回顾支出和分类，图片中均为演示数据'}
};
const image = document.querySelector('#app-preview');
document.querySelectorAll('[data-preview]').forEach(button => {
  button.addEventListener('click', () => {
    const preview = previews[button.dataset.preview];
    if (!preview || !image) return;
    image.src = preview.src;
    image.alt = preview.alt;
    document.querySelectorAll('[data-preview]').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
  });
});
