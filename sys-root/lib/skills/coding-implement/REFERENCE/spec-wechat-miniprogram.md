---
title: 微信小程序代码约束（Reference）
description: 当本次 coding-implement 的实现目标被明确为微信小程序时，AI 生成代码必须遵循的 WXML/WXSS/JS 原生语法与目录结构约束。
---

# 微信小程序代码约束（Reference）

## 适用条件
- 当本次 coding-implement 的实现目标被 `specs/*/spec.md` 或需求描述明确为「微信小程序」时适用。

## 强制约束
1. **技术栈限定（禁止框架语法）**
   - 强制遵循微信小程序原生语法规范；
   - 禁止使用 Vue/React 等框架语法；
   - 仅使用 `WXML + WXSS + JavaScript` 编写小程序代码。

2. **目录结构限定**
   - 严格遵循小程序目录结构：`app.js`/`app.json`/`app.wxss` + `pages/**/` 页面结构；
   - 页面路径与 `app.json` 中 `pages` 入口字段必须匹配且正确。

3. **WXML 约束**
   - WXML 仅使用小程序内置组件（如 `view/text/button/image/input` 等）；
   - 禁止自定义 HTML 标签。

4. **WXSS 约束**
   - WXSS 适配 `rpx` 响应式单位；
   - 禁止使用 `px` 作为全局单位；
   - 遵循小程序样式隔离规则。

5. **JavaScript 约束**
   - JS 逻辑仅调用小程序官方 API（`wx.xxx` 开头）；
   - 禁止使用浏览器 `DOM/BOM` API。

## 禁止项
- 禁止生成云开发、`npm` 依赖相关代码；
- 除非明确指令要求，否则不得引入额外能力/依赖。

## 交付要求
- 代码缩进规范、注释清晰，生成可直接运行的无语法错误代码；
- 生成代码后，简要说明文件存放路径和配置步骤。

