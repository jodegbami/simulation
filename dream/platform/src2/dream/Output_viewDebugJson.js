/*global console, rJS, RSVP, initGadgetMixin */
(function (window, rJS, RSVP, initGadgetMixin) {
  "use strict";

  var gadget_klass = rJS(window);
  initGadgetMixin(gadget_klass);
  gadget_klass
    /////////////////////////////////////////////////////////////////
    // Acquired methods
    /////////////////////////////////////////////////////////////////
    .declareAcquiredMethod("aq_getAttachment", "jio_getAttachment")

    /////////////////////////////////////////////////////////////////
    // declared methods
    /////////////////////////////////////////////////////////////////
    .declareMethod("render", function (options) {
      var gadget = this;
      this.props.jio_key = options.id;
      this.props.result = options.result;

      return gadget.aq_getAttachment({
        "_id": gadget.props.jio_key,
        "_attachment": "simulation.json"
      })
        .push(function (result_json) {
          var result = JSON.parse(result_json);
          gadget.props.element.querySelector(".json_input").textContent =
            JSON.stringify(result[gadget.props.result].input);
          gadget.props.element.querySelector(".json_output").textContent =
            JSON.stringify(result[gadget.props.result].result);
        });

    });

}(window, rJS, RSVP, initGadgetMixin));