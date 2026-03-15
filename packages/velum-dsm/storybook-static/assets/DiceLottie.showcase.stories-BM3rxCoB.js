import{_ as p}from"./preload-helper-Dp1pzeXC.js";import{j as e,C as S,f as c}from"./iframe-v_xVpIIQ.js";import{d as L}from"./dice-CXxLZEMz.js";import{S as b,a as h,b as s}from"./_helpers-j3YeHUq4.js";const D={title:"Assets/DiceLottie"};function i(o){const n=c.useRef(null);return c.useEffect(()=>{let d=!1,t=null;return(async()=>{const a=n.current;if(!a)return;const f=await p(()=>import("./index-BFCYMfbp.js"),[],import.meta.url);if(d)return;const x=f.DotLottie;t=new x({canvas:a,src:L,autoplay:!0,loop:!0})})(),()=>{var a;d=!0,(a=t==null?void 0:t.destroy)==null||a.call(t)}},[]),e.jsx("canvas",{ref:n,style:{width:`${o.size}px`,height:`${o.size}px`,display:"block"}})}const r={render:()=>e.jsx(b,{maxWidth:"980px",children:e.jsx(S,{title:"Dice Lottie Showcase",subtitle:"Standardized references for loader usage at different scales.",children:e.jsxs(h,{children:[e.jsx(s,{label:"Tiny Loader",description:"Inline status or badge-sized motion",children:e.jsx(i,{size:18})}),e.jsx(s,{label:"Button Loader",description:"Action feedback inside a button",children:e.jsx(i,{size:24})}),e.jsx(s,{label:"Global Loader",description:"Large wait-state animation for full-screen overlays",children:e.jsx(i,{size:120})})]})})})};var l,u,m;r.parameters={...r.parameters,docs:{...(l=r.parameters)==null?void 0:l.docs,source:{originalSource:`{
  render: () => <StoryFrame maxWidth="980px">
      <Card title="Dice Lottie Showcase" subtitle="Standardized references for loader usage at different scales.">
        <StateMatrix>
          <StateCase label="Tiny Loader" description="Inline status or badge-sized motion">
            <DiceLottiePreview size={18} />
          </StateCase>
          <StateCase label="Button Loader" description="Action feedback inside a button">
            <DiceLottiePreview size={24} />
          </StateCase>
          <StateCase label="Global Loader" description="Large wait-state animation for full-screen overlays">
            <DiceLottiePreview size={120} />
          </StateCase>
        </StateMatrix>
      </Card>
    </StoryFrame>
}`,...(m=(u=r.parameters)==null?void 0:u.docs)==null?void 0:m.source}}};const _=["Showcase"];export{r as Showcase,_ as __namedExportsOrder,D as default};
