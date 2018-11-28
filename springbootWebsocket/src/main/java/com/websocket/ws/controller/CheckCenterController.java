package com.websocket.ws.controller;

import com.websocket.ws.service.WebSocketServer;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import javax.servlet.http.HttpServletRequest;
import java.io.IOException;

/**
 * @author sxj
 * @date 2018-11-27 19:42
 */
@Controller
@RequestMapping("/websocket")
public class CheckCenterController {
    /**
     * 页面请求
     *
     * @return
     */
    @RequestMapping("/socket/{id}")
    public String index(@PathVariable("id") int id, HttpServletRequest request) {
        System.out.println("==============" + id);
        request.setAttribute("cid", id);
        return "index";
    }

    /**
     * 推送数据接口
     *
     * @param cid
     * @param message
     * @return
     */
    @ResponseBody
    @RequestMapping("/push/{cid}")
    public String pushToWeb(@PathVariable String cid, String message) {
        try {
            WebSocketServer.sendInfo(message, cid);
        } catch (IOException e) {
            e.printStackTrace();
            return cid + "#" + e.getMessage();
        }
        return cid;
    }
}
