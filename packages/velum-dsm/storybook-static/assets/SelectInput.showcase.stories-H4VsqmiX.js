import{j as e,k as a}from"./iframe-v_xVpIIQ.js";import{S as i,a as s,b as n}from"./_helpers-j3YeHUq4.js";import"./preload-helper-Dp1pzeXC.js";const u={title:"Components/SelectInput"},t={render:()=>e.jsx(i,{maxWidth:"980px",children:e.jsxs(s,{children:[e.jsx(n,{label:"Default",description:"Standard select with short options",children:e.jsxs(a,{defaultValue:"translator",children:[e.jsx("option",{value:"translator",children:"Translator"}),e.jsx("option",{value:"formatter",children:"Formatter"}),e.jsx("option",{value:"timeline",children:"Timeline"})]})}),e.jsx(n,{label:"Long Options",description:"Long labels remain readable",children:e.jsxs(a,{defaultValue:"modern",children:[e.jsx("option",{value:"modern",children:"Modern Lexicon and Reference Materials"}),e.jsx("option",{value:"fantasy",children:"Fantasy Bestiary and Spell Catalog"})]})}),e.jsx(n,{label:"Disabled",description:"Unavailable select state",children:e.jsx(a,{defaultValue:"locked",disabled:!0,children:e.jsx("option",{value:"locked",children:"Selection locked"})})})]})})};var l,o,r;t.parameters={...t.parameters,docs:{...(l=t.parameters)==null?void 0:l.docs,source:{originalSource:`{
  render: () => <StoryFrame maxWidth="980px">
      <StateMatrix>
        <StateCase label="Default" description="Standard select with short options">
          <SelectInput defaultValue="translator">
            <option value="translator">Translator</option>
            <option value="formatter">Formatter</option>
            <option value="timeline">Timeline</option>
          </SelectInput>
        </StateCase>
        <StateCase label="Long Options" description="Long labels remain readable">
          <SelectInput defaultValue="modern">
            <option value="modern">Modern Lexicon and Reference Materials</option>
            <option value="fantasy">Fantasy Bestiary and Spell Catalog</option>
          </SelectInput>
        </StateCase>
        <StateCase label="Disabled" description="Unavailable select state">
          <SelectInput defaultValue="locked" disabled>
            <option value="locked">Selection locked</option>
          </SelectInput>
        </StateCase>
      </StateMatrix>
    </StoryFrame>
}`,...(r=(o=t.parameters)==null?void 0:o.docs)==null?void 0:r.source}}};const m=["Showcase"];export{t as Showcase,m as __namedExportsOrder,u as default};
