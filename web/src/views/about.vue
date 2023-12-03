<template>
  <div class="container">
    <div class="introduce-content">
      <h2>Proxy API <span style="font-size: 14px;color: #4a4a4a">(转发中间件服务)</span> </h2>
      <p>✊ 打造统一的AI接口服务中间件, 通过统一的接口, 转发到各个AI接口服务, 从而实现统一管理, 降低接口适配成本.</p>
      <p>💥 接口全部统一继承使用OpenAI的接口规范, 以便于后续模型的迁移, <b>但返回参数需要根据各个接口服务的返回参数进行适配.</b></p>
      <p>✨ 此服务中间件仅做转发, <b>不做计费处理</b>.</p>
      <p>🤡 GitHub: <a href="https://github.com/RipperTs/ai-proxy-api" target="_blank">https://github.com/RipperTs/ai-proxy-api</a></p>

      <h3>支持模型</h3>
      <p>✅ 支持官方 <b>Function Calling</b>，一眼辨别真假官方</p>
      <p>✅ GPT-3.5所有版本以及Embedding模型（支持最新gpt-3.5-turbo-1106模型）</p>
      <p>✅ GPT-4所有版本（支持最新gpt-4-1106-preview，也就是gpt-4-turbo，支持128k上下文）</p>
      <p>✅ GPT-4-32K所有版本</p>
      <p>✅ GPT-4 PLUS 模型：一键集成官方最新的gpt-4-turbo（知识库到2023年4月）、联网、多模态识别分析图片、生成图片（模型名称：gpt-4-all）</p>
      <p>✅ OpenAI文本转语音模型TTS：（模型名称：tts-1、tts-1-1106、tts-1-hd、tts-1-hd-1106）</p>
      <p>✅ OpenAI语音转文本模型Whisper：（模型名称：whisper-1）</p>
      <p>✅ 官方PLUS的GPTs接口（首发支持，模型名称：gpt-4-gizmo-(gizmo_id)，gizmo_id创建GPTs之后，分享链接中能看到g-xxxx）</p>
      <p>✅ 官方4V接口（模型名称：gpt-4-vision-preview，点击查看接入文档）</p>
      <p>✅ Midjourney、Stable-Diffusion官方接口（Imagine指令折合0.2元/次，U和V指令折合0.04元/次，快速模式，已集成了图片国内反代+Discord国内反代+中文翻译接口，模型名称：midjourney、stable-diffusion）</p>
      <p>✅ DALL·E官方接口（首发支持，点击查看接入文档，模型名称：dall-e-3、dall-e-2）</p>

      <h3>马上开始</h3>
      <p>点击 <a href="https://ai.wslmf.com">聊天</a> 即可马上体验，接口地址：<b>https://aikey.wslmf.com</b></p>
      <p>在【设置-API Key】粘贴后台生成的令牌，模型选gpt-4，即可使用（非默认模型请在自定义模型输入模型名称并选择即可）</p>
      <p style="color: #005cc5;font-weight: 500;">测试其他模型时建议关闭设置中的注入系统级提示信息，否则他都会说自己是ChatGPT</p>

      <h3>接入指南</h3>
      <p>修改应用 BASE_URL为中转接口调用地址：<b style="color: red;">https://aikey.wslmf.com</b>（对应 <b>https://api.openai.com</b>，如果原来接口地址需要加/v1的话我们的接口地址也需要在后面加/v1）</p>
      <p>例如:</p>
      <li style="color: #00aba9;">原来的:  <b>https://api.openai.com/v1/chat/completions</b></li>
      <li style="color: #3a8ee6;">现在的: <b>https://aikey.wslmf.com/v1/chat/completions</b></li>
      <br>
      <p>然后 API Key 也对应更换为本站后台自己生成的令牌</p>
      <br>

      <h3>常见问题</h3>
      <div class="common-problem">
        <p class="question">Q：切换到了GPT-4，询问它是不是GPT-4，为什么回答不是？</p>
        <div>A：首先如果你问GPT-4：你是不是GPT4？它大概率会回答：我是OpenAI的GPT-3 模型。之所以会这样，是因为OpenAI开放给API调用的GPT-4，训练数据都是2021年9月之前的。模型训练好之后，如果不重新训练，并不会自动更新里面的知识，这就好像我问2021年的你2023年第一顿饭你吃了什么，答案一定是错的。</div>
      </div>

      <div class="common-problem">
        <p class="question">Q：为什么ChatGPT Plus的GPT-4回答能回答出自己是GPT-4？</p>
        <div>A：简单来说，ChatGPT Plus使用的模型版本和开放给API的并不一样，作为内部版本，很大可能会用更新的数据去训练，甚至是实时数据训练。虽然都叫GPT-4，但给出的答案不同，因为训练数据不同。</div>
      </div>

      <div class="common-problem">
        <p class="question">Q：那我如何去判断他是否是GPT-4模型</p>
        <div>A：可使用以下逻辑性问题进行测试 问题 ： 鲁迅和周树人是什么关系 GPT-3.5：鲁迅和周树人是两个不同的人 GPT-4：鲁迅和周树人是同一个人</div>
      </div>

    </div>
  </div>
</template>

<script>
import Header from "@/components/Header.vue";

export default {
  components: {
    Header
  },
  data() {
    return {}
  },
  computed: {},
  watch: {},
  created() {

  },
  mounted() {
    let _this = this;

  },
  methods: {},

  //切记页面销毁需要销毁
  destroyed() {
    let _this = this
  },
}
</script>
<style lang="scss" scoped>
.introduce-content {
  background: #fff;
  border-radius: 6px;
  padding: 20px;
  margin-top: 30px;
  margin-bottom: 80px;
  p{
    line-height: 1.8rem;
  }
  .question{
    font-weight: 500;
    color: #ff5656;
  }
  .common-problem{
    margin-top: 16px;
  }
}
</style>
