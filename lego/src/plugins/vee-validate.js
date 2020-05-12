import { extend } from "vee-validate";
import {
  required,
  alpha,
  email,
  confirmed,
  min,
  max,
  alpha_num,
  length
} from "vee-validate/dist/rules";
import { localize } from "vee-validate";
import ko from "vee-validate/dist/locale/ko.json";

localize("ko", ko);

// Install required rule and message.
extend("required", required);

// Install alpha rule and message.
extend("alpha", alpha);

// Install email rule and message.
extend("email", email);

// Install confirmed rule and message.
extend("confirmed", confirmed);

// Install min rule and message.
extend("min", min);

// Install max rule and message.
extend("max", max);

extend("length", length);
// Custom password rule and message.
extend("alpha_num", alpha_num);

extend("password", {
  validate: str => {
    var pattern = new RegExp(
      "^(?=.*[a-z])(?=.*[0-9])(?=.*[!@#$%^&*])[A-Za-z0-9!@#$%^&*]"
    );
    return !!pattern.test(str);
  },
  message: "소문자, 숫자, 특수문자가 최소 하나 포함되어야 합니다"
});

extend("nickname", {
  validate: str => {
    var pattern = new RegExp("^(?=.*[가-힣])[가-힣]");
    return !!pattern.test(str);
  },
  message: "한글만 가능합니다"
});
